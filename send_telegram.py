# send_telegram.py

import requests

BOT_TOKEN = "7673667307:AAHxupSKq1xC-QP2Pl6q_wQEXSJMzwuefCU"
CHAT_ID = "2130752167"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)
