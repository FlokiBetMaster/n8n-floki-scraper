import requests

url = 'https://n8n-floki.onrender.com/webhook/apuesta'

data = {
    "competition": "Copa Libertadores",
    "teams": "Flamengo vs Millonarios",
    "odds": "86",
    "stake": "3"
}

response = requests.post(url, json=data)
print("✅ Respuesta del webhook:", response.status_code)
