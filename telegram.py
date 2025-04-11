import requests

BOT_TOKEN = "7673667307:AAHxupSKq1xC-QP2Pl6q_wQEXSJMzwuefCU"
CHAT_ID = "2130752167"

def send_to_telegram(match):
    text = f"⚽ ¡Nueva Apuesta Recomendada!\n"            f"📍 Partido: {match['teams']}\n"            f"🎯 Apuesta: {match['tipo']}\n"            f"💸 Cuota: {match['cuota']}\n"            f"🔥 Confianza: {match['confianza']}%\n"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    })
