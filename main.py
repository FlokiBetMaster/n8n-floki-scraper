@"
import requests

# ========== ⚙️ CONFIGURACIÓN ==========
TELEGRAM_TOKEN = "7673667307:AAHxupSKq1xC-QP2Pl6q_wQEXSJMzwuefCU"
CHAT_ID = "2130752167"
URL = "https://www.goal.com/en/live-scores"  # o el sitio real que estés scrapeando

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def obtener_datos():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print("❌ Error al obtener datos:", e)
        return None

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=data)
        print("✅ Mensaje enviado:", r.status_code)
    except Exception as e:
        print("❌ Error al enviar mensaje:", e)

def main():
    print("🚀 Ejecutando bot Floki...")
    html = obtener_datos()

    if html and len(html) > 100:
        enviar_telegram("⚽ *FlokiBot activo!* Contenido recibido correctamente.")
    else:
        enviar_telegram("⚠️ *FlokiBot detectó error:* No se pudo obtener datos del sitio.")

if __name__ == "__main__":
    main()
"@ | Out-File -Encoding utf8 main.py
