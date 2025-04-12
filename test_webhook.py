import requests

url = "https://flokibetmaster.app.n8n.cloud/webhook-test/apuesta"  # Reemplaza con tu URL real

data = {
    "competition": "Brasileirão Série A",
    "teams": "Flamengo vs Palmeiras",
    "odds": 92,
    "stake": "12.000 COP"
}

response = requests.post(url, json=data)
print("✅ Respuesta del webhook:", response.status_code)
