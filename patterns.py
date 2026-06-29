def detect_patterns(df):

    # Bullish Engulfing
    df["BULL_ENGULFING"] = (
        (df["close"] > df["open"]) &
        (df["close"].shift(1) < df["open"].shift(1)) &
        (df["open"] < df["close"].shift(1)) &
        (df["close"] > df["open"].shift(1))
    )

    # Bearish Engulfing
    df["BEAR_ENGULFING"] = (
        (df["close"] < df["open"]) &
        (df["close"].shift(1) > df["open"].shift(1)) &
        (df["open"] > df["close"].shift(1)) &
        (df["close"] < df["open"].shift(1))
    )

    # Hammer
    body = (df["close"] - df["open"]).abs()

    lower_shadow = (
        df[["open", "close"]].min(axis=1)
        - df["low"]
    )

    upper_shadow = (
        df["high"]
        - df[["open", "close"]].max(axis=1)
    )

    df["HAMMER"] = (
        (lower_shadow > body * 2) &
        (upper_shadow < body)
    )

    # Shooting Star
    df["SHOOTING_STAR"] = (
        (upper_shadow > body * 2) &
        (lower_shadow < body)
    )

    return df