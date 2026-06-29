def detect_structure(df):

    highs = df["high"]
    lows = df["low"]

    bos_up = highs.iloc[-1] > highs.iloc[-2]
    bos_down = lows.iloc[-1] < lows.iloc[-2]

    return bos_up, bos_down