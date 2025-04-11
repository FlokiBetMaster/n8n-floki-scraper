def calculate_stake(prob):
    if prob >= 70:
        return 2
    elif prob >= 60:
        return 3
    elif prob >= 50:
        return 4
    elif prob >= 40:
        return 5
    elif prob >= 30:
        return 6
    elif prob >= 20:
        return 7
    elif prob >= 10:
        return 8
    else:
        return 10
