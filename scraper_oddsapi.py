import requests

API_KEY = "a6fdcc949cb6e52a9f9fbbfff6e44b30"
CHAT_ID = "2130752167"
BOT_TOKEN = "7673667307:AAHxupSKq1xC-QP2Pl6q_wQEXSJMzwuefCU"

sports = [
    "soccer_conmebol_copa_libertadores",
    "soccer_conmebol_copa_sudamericana"
]

markets = "h2h,spreads,totals"
regions = "us"

print("[📡 Buscando apuestas de valor...]")

def calcular_stake(probabilidad):
    if probabilidad >= 70:
        return 10
    elif probabilidad >= 60:
        return 8
    elif probabilidad >= 50:
        return 6
    elif probabilidad >= 40:
        return 4
    else:
        return 2

def enviar_a_telegram(apuesta):
    mensaje = f"""
⚽ ¡Nueva Apuesta Recomendada!
📍 Partido: {apuesta['teams']}
🎯 Apuesta: {apuesta['tipo']}
💸 Cuota: {apuesta['cuota']}
🔥 Confianza: {apuesta['odds']}%
📊 Stake sugerido: {apuesta['stake']}
"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(url, json=payload)
        print("🚀 Enviado a Telegram:", res.status_code)
    except Exception as e:
        print("❌ Error al enviar a Telegram:", e)

def buscar_apuestas_valor():
    apuestas_finales = {}

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
                mejor_apuesta = None

                for bookmaker in evento["bookmakers"]:
                    for mercado in bookmaker["markets"]:
                        for outcome in mercado["outcomes"]:
                            cuota = outcome["price"]
                            if cuota > 1.5:
                                probabilidad = round(100 / cuota, 2)
                                stake = calcular_stake(probabilidad)
                                apuesta = {
                                    "teams": equipos,
                                    "tipo": outcome["name"],
                                    "odds": probabilidad,
                                    "cuota": cuota,
                                    "stake": stake
                                }

                                if not mejor_apuesta or apuesta["odds"] > mejor_apuesta["odds"]:
                                    mejor_apuesta = apuesta

                if mejor_apuesta:
                    apuestas_finales[equipos] = mejor_apuesta

        except Exception as e:
            print("❌ Error:", e)
            continue

    return apuestas_finales.values()

# Ejecutar
apuestas = buscar_apuestas_valor()

if apuestas:
    for apuesta in apuestas:
        print(f"📢 Apuesta Recomendada: {apuesta['teams']} - {apuesta['tipo']} ({apuesta['odds']}%)")
        enviar_a_telegram(apuesta)
else:
    print("🔍 No se encontraron apuestas de valor para hoy.")
