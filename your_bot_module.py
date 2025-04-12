# your_bot_module.py

import requests
import time
from datetime import datetime
from send_telegram import send_message  # Debes tener este módulo ya listo

# Tu API KEY de ODDS API
API_KEY = "TU_API_KEY_ODDSAPI"
REGIONS = "sa"  # Sudamérica
MARKETS = "h2h"
BOOKMAKERS = "bwin"  # O el que estés usando
SPORT = "soccer"
LEAGUES = ["Copa Libertadores", "Copa Sudamericana"]

def is_value_bet(odds, implied_prob, confidence_threshold=0.75):
    """Apuesta de valor: si la probabilidad implícita es mayor al inverso de la cuota"""
    return implied_prob > (1 / odds) and implied_prob >= confidence_threshold

def get_confidence_level(team_rating, opponent_rating):
    """Simula análisis para determinar confianza (esto puede reemplazarse con un modelo real)"""
    delta = team_rating - opponent_rating
    base_conf = 0.5 + delta * 0.1
    return max(min(base_conf, 0.95), 0.5)

def start_bot():
    while True:
        try:
            url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?regions={REGIONS}&markets={MARKETS}&bookmakers={BOOKMAKERS}&apiKey={API_KEY}"
            response = requests.get(url)
            games = response.json()

            for game in games:
                league = game.get("league", {}).get("name", "")
                if not any(l in league for l in LEAGUES):
                    continue

                home = game["home_team"]
                away = game["away_team"]
                commence_time = datetime.fromisoformat(game["commence_time"].replace("Z", "+00:00"))
                match_time = commence_time.strftime("%H:%M %d/%m")

                for bookmaker in game["bookmakers"]:
                    for market in bookmaker["markets"]:
                        for outcome in market["outcomes"]:
                            team = outcome["name"]
                            odds = outcome["price"]

                            # Simula niveles de rating por nombre (puedes usar Elo real luego)
                            confidence = get_confidence_level(len(home), len(away)) if team == home else get_confidence_level(len(away), len(home))

                            if is_value_bet(odds, confidence):
                                mensaje = f"""
📢 *APUESTA DE VALOR SEGURA DETECTADA* ⚠️

🏆 Torneo: {league}
🕒 Hora: {match_time}
⚔️ Partido: {home} vs {away}
📈 Apuesta: Gana *{team}*
💰 Cuota: {odds}
🔒 Confianza: {int(confidence * 100)}%

🔥 Verifica en Bwin o tu casa de apuestas favorita
"""
                                send_message(mensaje.strip())
                                print("[✔️ FlokiBot] Enviada al Telegram:", home, "vs", away)

            time.sleep(600)  # Espera 10 minutos antes de volver a escanear

        except Exception as e:
            print("[❌ FlokiBot] Error al obtener datos:", str(e))
            time.sleep(30)
