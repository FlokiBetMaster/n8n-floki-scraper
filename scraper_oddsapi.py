import requests

API_KEY = "a6fdcc949cb6e52a9f9fbbfff6e44b30"
BOT_TOKEN = "7673667307:AAHxupSKq1xC-QP2Pl6q_wQEXSJMzwuefCU"
CHAT_ID = "2130752167"

sports = [
    "soccer_conmebol_copa_libertadores",
    "soccer_conmebol_copa_sudamericana"
]

markets = "h2h,spreads,totals"
regions = "us"
webhook_url = "https://n8n-floki.onrender.com/webhook/apuesta"

print("[📡 Buscando apuestas de valor...]")

def calcular_stake(probabilidad):
    if probabilidad > 50:
        return 10
    elif probabilidad > 40:
        return 20
    elif probabilidad > 30:
        return 30
    elif probabilidad > 20:
        return 40
    elif probabilidad > 10:
        return 60
    else:
        return 100 + (10 - probabilidad) * 1.5

def send_to_telegram(apuesta):
    message = (
        f"⚽ *¡Nueva Apuesta Recomendada!*\n\n"
        f"📍 *Partido:* {apuesta['teams']}\n"
        f"🎯 *Apuesta:* {apuesta['tipo']}\n"
        f"📈 *Probabilidad:* {apuesta['odds']:.2f}%\n"
        f"💰 *Stake sugerido:* {round(apuesta['stake'])}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload)
        print("📨 Telegram:", response.status_code)
    except Exception as e:
        print("❌ Error en Telegram:", e)

def buscar_apuestas_valor():
    apuestas_valor = []

    for sport in sports:
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
        params = {
            "apiKey": API_KEY,
            "regions": regions,
            "markets": markets,
            "oddsFormat": "decimal"
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if isinstance(data, dict) and "error_code" in data:
                print("Error:", data)
                continue

            for evento in data:
                equipos = evento["home_team"] + " vs " + evento["away_team"]
                for bookmaker in evento["bookmakers"]:
                    for mercado in bookmaker["markets"]:
                        for outcome in mercado["outcomes"]:
                            cuota = outcome["price"]
                            if cuota > 2.0:
                                probabilidad = 100 / cuota
                                stake = calcular_stake(probabilidad)
                                apuesta = {
                                    "teams": equipos,
                                    "odds": probabilidad,
                                    "stake": stake,
                                    "tipo": outcome["name"]
                                }
                                apuestas_valor.append(apuesta)

        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            continue

    return apuestas_valor

# Ejecutar
apuestas_valor = buscar_apuestas_valor()

if apuestas_valor:
    for apuesta in apuestas_valor:
        print(f"📢 Apuesta de Valor Encontrada:")
        print(f"🆚 Partido: {apuesta['teams']}")
        print(f"🎯 Tipo: {apuesta['tipo']}")
        print(f"📈 Probabilidad: {apuesta['odds']:.2f}%")
        print(f"💰 Stake sugerido: {apuesta['stake']}")
        print("-" * 30)

        # Enviar a webhook de n8n
        payload = {
            "teams": apuesta["teams"],
            "odds": round(apuesta["odds"], 2),
            "stake": apuesta["stake"],
            "competition": "Copa Libertadores / Sudamericana"
        }
        try:
            res = requests.post(webhook_url, json=payload)
            print(f"🚀 Enviado a n8n: {res.status_code}")
        except Exception as e:
            print(f"❌ Error al enviar a n8n:", e)

        # Enviar también a Telegram directo
        send_to_telegram(apuesta)
else:
    print("🔍 No se encontraron apuestas de valor para hoy.")
