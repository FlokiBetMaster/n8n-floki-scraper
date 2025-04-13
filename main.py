import time
from fetch_odds import fetch_odds
from predict import get_best_bet_per_match
from stake_manager import calculate_stake
from telegram import send_telegram_message

print("🔥 Floki está en modo automático...")

while True:
    try:
        print("📡 [Buscando apuestas en vivo...]")
        events = fetch_odds()
        best_bets = get_best_bet_per_match(events)

        for bet in best_bets:
            bet["stake"] = calculate_stake(bet["odds"])
            print(f"📢 Enviando apuesta: {bet}")
            status = send_telegram_message(bet)
            print(f"🚀 Enviado a Telegram: {status}")

        print("⏱️ Esperando 60 segundos para el siguiente análisis...\n")
        time.sleep(60)

    except Exception as e:
        print(f"❌ Error en el loop: {e}")
        time.sleep(60)
