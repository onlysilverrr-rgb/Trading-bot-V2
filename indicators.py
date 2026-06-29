
import pandas as pd


def add_indicators(data):

    if not data or "values" not in data:
        return None

    df = pd.DataFrame(data["values"])

    if df.empty:
        return None

    # Convert numeric columns
    for col in ["open", "high", "low", "close"]:

        df[col] = df[col].astype(float)

    if "volume" in df.columns:

        df["volume"] = df["volume"].astype(float)

    # Oldest candle first
    df = df.iloc[::-1].reset_index(drop=True)

    ####################################################
    # EMA
    ####################################################

    df["EMA20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["EMA200"] = df["close"].ewm(span=200, adjust=False).mean()

    ####################################################
    # RSI
    ####################################################

    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = 100 - (100 / (1 + rs))

    ####################################################
    # MACD
    ####################################################

    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()

    df["MACD"] = ema12 - ema26
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()

    ####################################################
    # Bollinger Bands
    ####################################################

    df["BB_MIDDLE"] = df["close"].rolling(20).mean()

    std = df["close"].rolling(20).std()

    df["BB_UPPER"] = df["BB_MIDDLE"] + (2 * std)
    df["BB_LOWER"] = df["BB_MIDDLE"] - (2 * std)

    ####################################################
    # ATR
    ####################################################

    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()

    tr = pd.concat(
        [high_low, high_close, low_close],
        axis=1
    ).max(axis=1)

    df["ATR"] = tr.rolling(14).mean()

    ####################################################
    # ADX
    ####################################################

    plus_dm = df["high"].diff()
    minus_dm = -df["low"].diff()

    plus_dm = plus_dm.where(
        (plus_dm > minus_dm) & (plus_dm > 0),
        0
    )

    minus_dm = minus_dm.where(
        (minus_dm > plus_dm) & (minus_dm > 0),
        0
    )

    atr14 = tr.rolling(14).mean()

    plus_di = 100 * (
        plus_dm.rolling(14).mean() / atr14
    )

    minus_di = 100 * (
        minus_dm.rolling(14).mean() / atr14
    )

    dx = (
        (plus_di - minus_di).abs()
        / (plus_di + minus_di)
    ) * 100

    df["ADX"] = dx.rolling(14).mean()

    ####################################################
    # VWAP
    ####################################################

    if "volume" in df.columns:

        typical_price = (
            df["high"] +
            df["low"] +
            df["close"]
        ) / 3

        df["VWAP"] = (
            (typical_price * df["volume"]).cumsum()
            / df["volume"].cumsum()
        )

        df["VOLUME_MA20"] = (
            df["volume"].rolling(20).mean()
        )

    ####################################################
    # Remove NaN rows
    ####################################################

    df = df.dropna().reset_index(drop=True)

    return df

