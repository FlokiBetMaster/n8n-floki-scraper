from fetch_odds import fetch_odds
from predict import get_best_bet_per_match
from stake_manager import calculate_stake
from telegram import send_telegram_message

def main():
    print("📡 [ Cargando partidos... ]")
    events = fetch_odds()
    print(f"✅ [ Partidos encontrados: {len(events)} ]")
    best_bets = get_best_bet_per_match(events)

    for bet in best_bets:
        bet["stake"] = calculate_stake(bet["odds"])
        print(f"📢 Apuesta: {bet}")
        status = send_telegram_message(bet)
        print(f"🚀 Enviado a Telegram: {status}")

if __name__ == "__main__":
    main()
