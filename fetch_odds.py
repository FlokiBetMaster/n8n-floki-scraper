import requests

API_KEY = "a6fdcc949cb6e52a9f9fbbfff6e44b30"
SPORTS = [
    "soccer_brazil_campeonato", "soccer_argentina_primera_division",
    "soccer_uefa_champs_league", "soccer_epl", "soccer_la_liga",
    "soccer_serie_a", "soccer_ligue_one", "soccer_bundesliga"
]
MARKETS = "h2h,totals,btts,asian_handicap"
REGIONS = "eu"

def fetch_odds():
    matches = []
    for sport in SPORTS:
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
        params = {
            "apiKey": API_KEY,
            "regions": REGIONS,
            "markets": MARKETS,
            "oddsFormat": "decimal"
        }
        try:
            res = requests.get(url, params=params)
            if res.status_code == 200:
                data = res.json()
                matches.extend(data)
        except Exception as e:
            print("❌ Error en fetch_odds:", e)
    return matches
