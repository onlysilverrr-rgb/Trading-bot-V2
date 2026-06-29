def detect_liquidity_sweep(df):

    high = df["high"]
    low = df["low"]
    close = df["close"]

    # previous candle levels
    prev_high = high.iloc[-2]
    prev_low = low.iloc[-2]

    current_close = close.iloc[-1]
    current_high = high.iloc[-1]
    current_low = low.iloc[-1]

    # Liquidity sweep up (fake breakout above resistance then rejection)
    sweep_up = (
        current_high > prev_high and
        current_close < prev_high
    )

    # Liquidity sweep down (fake breakdown below support then recovery)
    sweep_down = (
        current_low < prev_low and
        current_close > prev_low
    )

    return sweep_up, sweep_down