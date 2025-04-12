import requests

TOKEN = "7673667307:AAHxupSKq1xC-QP2Pl6q_wQEXSJMzwuefCU"
CHAT_ID = "2130752167"

def send_telegram_message(bet):
    msg = f"⚽ *Apuesta Recomendada*
"           f"📍 Partido: {bet['teams']}
"           f"🎯 Apuesta: {bet['type']}
"           f"📈 Probabilidad: {bet['odds']}%
"           f"💸 Stake: {bet['stake']}
"           f"_Por FlokiBot_"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    })
    return res.status_code
