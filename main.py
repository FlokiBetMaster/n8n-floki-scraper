from fetch_odds import fetch_odds
from predict import select_best_bet
from stake_manager import calculate_stake
from telegram import send_to_telegram

def main():
    print("[📡 Cargando partidos...]")
    matches = fetch_odds()
    print(f"[✅ Partidos encontrados: {len(matches)}]")
    predictions = select_best_bet(matches)

    for pred in predictions:
        prob = round(100 / pred['cuota'], 2)
        stake = calculate_stake(prob)
        pred["confianza"] = prob
        pred["stake"] = stake
        print(f"📢 {pred['teams']} | {pred['tipo']} | Cuota: {pred['cuota']} | Confianza: {prob}% | Stake: {stake}")
        send_to_telegram(pred)

if __name__ == "__main__":
    main()
