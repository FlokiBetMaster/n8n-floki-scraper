import requests

API_KEY = "a6fdcc949cb6e52a9f9fbbfff6e44b30"
SPORTS = [
    "soccer_epl", "soccer_serie_a", "soccer_laliga", "soccer_ligue_one",
    "soccer_bundesliga", "soccer_brazil_campeonato", "soccer_argentina_superliga"
]
MARKETS = "h2h,totals,both_teams_to_score,asian_handicap"
REGIONS = "eu"
def fetch_odds():
    all_events = []
    for sport in SPORTS:
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
        params = {
            "apiKey": API_KEY,
            "regions": REGIONS,
            "markets": MARKETS,
            "oddsFormat": "decimal"
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                all_events.extend(response.json())
        except Exception as e:
            print(f"[❌ Error en {sport}]:", e)
    return all_events
