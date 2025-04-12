from fetch_odds import fetch_odds
from predict import get_best_bet_per_match
from stake_manager import calculate_stake, update_bank
from telegram import send_telegram_message

def main():
    print("📡 [ Cargando partidos en vivo...]")
    events = fetch_odds()
    print(f"✅ [ Partidos encontrados: {len(events)} ]")
    best_bets = get_best_bet_per_match(events)
    bank = 100000

    for bet in best_bets:
        bet["stake"] = calculate_stake(bet["odds"], bank)
        bank = update_bank(bank, bet["stake"])["new_bank"]
        print(f"📢 Apuesta: {bet}")
        send_telegram_message(bet)

if __name__ == "__main__":
    main()
