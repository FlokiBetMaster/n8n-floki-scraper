def get_best_bet_per_match(events):
    best_bets = []
    seen = set()
    for event in events:
        teams = f"{event['home_team']} vs {event['away_team']}"
        best = None
        highest_prob = 0
        for book in event.get("bookmakers", []):
            for market in book.get("markets", []):
                for out in market.get("outcomes", []):
                    prob = 100 / out["price"]
                    if prob > highest_prob:
                        highest_prob = prob
                        best = {
                            "teams": teams,
                            "type": out["name"],
                            "odds": round(prob, 2)
                        }
        if best and teams not in seen:
            best_bets.append(best)
            seen.add(teams)
    return best_bets
