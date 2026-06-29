
def get_support_resistance(df, lookback=20):

    recent = df.tail(lookback)

    support = recent["low"].min()

    resistance = recent["high"].max()

    return support, resistance


def is_breakout(df, resistance):

    if resistance is None:
        return False

    last_close = df.iloc[-1]["close"]

    previous_close = df.iloc[-2]["close"]

    return (
        previous_close <= resistance and
        last_close > resistance
    )


def is_breakdown(df, support):

    if support is None:
        return False

    last_close = df.iloc[-1]["close"]

    previous_close = df.iloc[-2]["close"]

    return (
        previous_close >= support and
        last_close < support
    )
