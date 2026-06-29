import json

FILE = "performance.json"


def load():

    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {"wins": 0, "losses": 0, "total": 0}


def save(data):

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def update_trade_result(win=True):

    data = load()

    data["total"] += 1

    if win:
        data["wins"] += 1
    else:
        data["losses"] += 1

    save(data)


def get_win_rate():

    data = load()

    if data["total"] == 0:
        return 0

    return round((data["wins"] / data["total"]) * 100, 2)