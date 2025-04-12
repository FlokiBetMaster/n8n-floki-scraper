def calculate_stake(prob, bank=100000):
    if prob > 50: return 1
    if prob > 40: return 2
    if prob > 30: return 3
    if prob > 20: return 5
    if prob > 10: return 7
    return 10

def update_bank(bank, stake):
    return {"new_bank": bank - stake}
