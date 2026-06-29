import json

LOG_FILE = "trade_log.json"


def log_trade(market, signal, confidence, entry, sl, tp):

    trade = {
        "market": market,
        "signal": signal,
        "confidence": confidence,
        "entry": entry,
        "sl": sl,
        "tp": tp
    }

    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(trade)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)