import requests

TELEGRAM_TOKEN = "7673667307:AAHxupSKq1xC-QP2Pl6q_wQEXSJMzwuefCU"
CHAT_ID = "2130752167"

message = "🧪 *Floki Test:* Este es un mensaje de prueba enviado desde Render."

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
res = requests.post(url, json={
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "Markdown"
})

print("Código de estado:", res.status_code)
print("Respuesta:", res.text)
