def select_best_bet(matches):
    predictions = []
    for event in matches:
        try:
            teams = f"{event['home_team']} vs {event['away_team']}"
            best_odd = 0
            best_pick = None
            for bookmaker in event["bookmakers"]:
                for market in bookmaker["markets"]:
                    for outcome in market["outcomes"]:
                        if outcome["price"] > best_odd:
                            best_odd = outcome["price"]
                            best_pick = {
                                "teams": teams,
                                "tipo": outcome["name"],
                                "cuota": best_odd
                            }
            if best_pick:
                predictions.append(best_pick)
        except Exception as e:
            print("❌ Error en predict:", e)
    return predictions
