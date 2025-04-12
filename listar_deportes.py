import requests

API_KEY = "a6fdcc949cb6e52a9f9fbbfff6e44b30"
url = f"https://api.the-odds-api.com/v4/sports/?apiKey={API_KEY}"

response = requests.get(url)

if response.status_code == 200:
    deportes = response.json()
    print("📋 Deportes disponibles que contienen 'libertadores' o 'sudamericana':\n")
    for d in deportes:
        if "libertadores" in d["title"].lower() or "sudamericana" in d["title"].lower() or \
           "libertadores" in d["description"].lower() or "sudamericana" in d["description"].lower():
            print(f"✅ {d['title']}  --->  {d['key']}")
else:
    print(f"❌ Error: {response.status_code} - {response.text}")
