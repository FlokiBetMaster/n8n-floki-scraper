import requests

TELEGRAM_TOKEN = "7673667307:AAHxupSKq1xC-QP2Pl6q_wQEXSJMzwuefCU"
CHAT_ID = "2130752167"

def send_telegram_message(bet):
    msg = (
        f"⚽ *Apuesta Recomendada*\n\n"
        f"📍 *Partido:* {bet['teams']}\n"
        f"🎯 *Apuesta:* {bet['type']}\n"
        f"📈 *Probabilidad:* {bet['odds']}%\n"
        f"💸 *Stake:* {bet['stake']}\n\n"
        f"_Enviado automáticamente por FlokiBot_"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    })

    return response.status_code
