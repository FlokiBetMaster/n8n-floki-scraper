from flask import Flask, jsonify
import requests
import json
import time
import telegram
from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import schedule
import threading
import logging

app = Flask(__name__)

# Configuración
ODDS_API_KEY = "a6fdcc949cb6e52a9f9fbbfff6e44b30"
ODDS_API_URL = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"
CACHE_FILE = "odds_cache.json"
TELEGRAM_TOKEN = "7673667307:AAHxupSKq1xC-QP2Pl6q_wQEXSJMzwuefCU"
TELEGRAM_CHAT_ID = "2130752167"
BANK_FILE = "bank.json"
bot = telegram.Bot(token=TELEGRAM_TOKEN)
logging.basicConfig(filename="flokibot.log", level=logging.INFO)

# Gestión de caché
def load_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"timestamp": 0, "data": []}

def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump({"timestamp": time.time(), "data": data}, f)

# Gestión de bank
def load_bank():
    try:
        with open(BANK_FILE, "r") as f:
            return json.load(f)
    except:
        return {"balance": 100000, "bets": []}

def save_bank(bank):
    with open(BANK_FILE, "w") as f:
        json.dump(bank, f)

# Lógica de predicción
def calcular_probabilidad(cuota):
    return round(100 / cuota, 2)

def es_value_bet(probabilidad, cuota):
    valor_esperado = (probabilidad / 100) * cuota
    return valor_esperado > 1.10

def calcular_stake_kelly(bank, odds, prob):
    b = odds - 1
    p = prob / 100
    q = 1 - p
    kelly_fraction = (b * p - q) / b
    return max(0, min(bank * kelly_fraction * 0.5, bank * 0.03))

def get_bwin_url(match):
    teams = match.lower().replace(" vs ", "-vs-")
    return f"https://www.bwin.com/es/sports/futbol-4/partido/{teams}"

# Endpoints Flask
@app.route("/matches")
def obtener_matches():
    cache = load_cache()
    if time.time() - cache["timestamp"] < 6 * 3600:
        return jsonify(cache["data"])
    
    response = requests.get(ODDS_API_URL, params={
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "h2h,totals"
    })
    if response.status_code == 200:
        matches = response.json()
        save_cache(matches)
        return jsonify(matches)
    return jsonify({"error": "No se pudieron obtener los partidos"}), 500

@app.route("/predictions")
def obtener_predictions():
    matches = load_cache()["data"]
    predictions = []
    for match in matches[:3]:
        home_team = match.get("home_team", "Unknown")
        away_team = match.get("away_team", "Unknown")
        try:
            h2h_odds = match["bookmakers"][0]["markets"][0]["outcomes"]
            home_odds = h2h_odds[0]["price"]
            prob = calcular_probabilidad(home_odds)
            if es_value_bet(prob, home_odds) and 1.5 <= home_odds <= 3.0:
                predictions.append({
                    "match": f"{home_team} vs {away_team}",
                    "bet": f"{home_team} gana",
                    "odds": home_odds,
                    "confidence": prob / 100,
                    "market": "1X2"
                })
            totals_odds = match["bookmakers"][0]["markets"][1]["outcomes"]
            over_odds = totals_odds[0]["price"]
            prob = calcular_probabilidad(over_odds)
            if es_value_bet(prob, over_odds) and 1.5 <= over_odds <= 3.0:
                predictions.append({
                    "match": f"{home_team} vs {away_team}",
                    "bet": "Over 2.5",
                    "odds": over_odds,
                    "confidence": prob / 100,
                    "market": "totals"
                })
        except (KeyError, IndexError):
            continue
    return jsonify(predictions)

# Telegram
def send_predictions_to_telegram():
    logging.info("Enviando predicciones a Telegram...")
    try:
        bank = load_bank()
        response = requests.get("http://localhost:5000/predictions")
        predictions = response.json()
        sent_matches = set()
        for pred in predictions:
            if pred["match"] not in sent_matches and len(sent_matches) < 3:
                sent_matches.add(pred["match"])
                stake = calcular_stake_kelly(bank["balance"], pred["odds"], pred["confidence"] * 100)
                message = (f"🏆 {pred['match']}\n"
                           f"Apuesta: {pred['bet']}\n"
                           f"Cuota: {pred['odds']}\n"
                           f"Stake: {stake:.2f} COP\n"
                           f"Confianza: {pred['confidence']*100:.1f}%")
                keyboard = [[InlineKeyboardButton("Apostar en Bwin", url=get_bwin_url(pred["match"]))]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, reply_markup=reply_markup)
                bank["bets"].append({
                    "match": pred["match"],
                    "bet": pred["bet"],
                    "stake": stake,
                    "odds": pred["odds"],
                    "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "result": "pending"
                })
                save_bank(bank)
        logging.info("Predicciones enviadas con éxito")
    except Exception as e:
        logging.error(f"Error: {e}")

def stats(update, context):
    bank = load_bank()
    message = (f"💰 Bank: {bank['balance']:.2f} COP\n"
               f"📊 Apuestas realizadas: {len(bank['bets'])}")
    update.message.reply_text(message)

def bets(update, context):
    bank = load_bank()
    if not bank["bets"]:
        update.message.reply_text("No hay apuestas registradas.")
        return
    message = "📜 Historial de apuestas:\n"
    for bet in bank["bets"][-5:]:
        message += f"{bet['date']} - {bet['match']} ({bet['bet']}): {bet['stake']:.2f} COP @ {bet['odds']} ({bet['result']})\n"
    update.message.reply_text(message)

def performance(update, context):
    bank = load_bank()
    initial_bank = 100000
    roi = ((bank["balance"] - initial_bank) / initial_bank) * 100
    update.message.reply_text(f"📈 ROI: {roi:.2f}%")

def result(update, context):
    bank = load_bank()
    if not bank["bets"]:
        update.message.reply_text("No hay apuestas para actualizar.")
        return
    try:
        args = context.args
        if len(args) != 2:
            update.message.reply_text("Uso: /result <índice> <win/lose>")
            return
        index = int(args[0]) - 1
        outcome = args[1].lower()
        if index < 0 or index >= len(bank["bets"]):
            update.message.reply_text("Índice inválido.")
            return
        bet = bank["bets"][index]
        if outcome == "win":
            bank["balance"] += bet["stake"] * (bet["odds"] - 1)
            bet["result"] = "win"
        elif outcome == "lose":
            bank["balance"] -= bet["stake"]
            bet["result"] = "lose"
        else:
            update.message.reply_text("Resultado debe ser 'win' o 'lose'.")
            return
        save_bank(bank)
        update.message.reply_text(f"Apuesta {index + 1} actualizada: {bet['match']} ({bet['result']}). Bank: {bank['balance']:.2f} COP")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Programar Telegram
schedule.every(6).hours.do(send_predictions_to_telegram)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

def start_telegram_bot():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("bets", bets))
    dp.add_handler(CommandHandler("performance", performance))
    dp.add_handler(CommandHandler("result", result))
    updater.start_polling()

if __name__ == "__main__":
    threading.Thread(target=start_telegram_bot, daemon=True).start()
    threading.Thread(target=run_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)