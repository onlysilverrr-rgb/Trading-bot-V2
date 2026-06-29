def detect_order_block(df):

    # Simple approximation:
    # last strong bullish/bearish candle zones

    prev = df.iloc[-2]
    last = df.iloc[-1]

    bullish_ob = (
        prev["close"] < prev["open"] and
        last["close"] > last["open"]
    )

    bearish_ob = (
        prev["close"] > prev["open"] and
        last["close"] < last["open"]
    )

    return bullish_ob, bearish_ob


def detect_fvg(df):

    # Fair Value Gap (simple 3 candle imbalance)

    if len(df) < 3:
        return False, False

    c1 = df.iloc[-3]
    c2 = df.iloc[-2]
    c3 = df.iloc[-1]

    bullish_fvg = c1["high"] < c3["low"]
    bearish_fvg = c1["low"] > c3["high"]

    return bullish_fvg, bearish_fvg