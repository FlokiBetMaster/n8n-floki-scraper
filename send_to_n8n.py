# send_to_n8n.py

import requests

WEBHOOK_URL = "https://n8n.yourdomain.com/webhook/floki/apuestas"  # Cambia por el tuyo

def send_to_n8n(data):
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        print("[📤] Enviado a n8n:", response.status_code)
    except Exception as e:
        print("[❌] Error enviando a n8n:", str(e))
