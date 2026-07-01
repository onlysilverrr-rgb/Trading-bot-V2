from support_resistance import get_support_resistance, is_breakout, is_breakdown
from market_structure import detect_structure
from liquidity import detect_liquidity_sweep
from smart_money import detect_order_block, detect_fvg
from news_filter import is_high_impact_news_time


def generate_signal(df15, df1h):

    news_block, _ = is_high_impact_news_time()

    if news_block:
        return "HOLD", 0, ["High impact news detected"], None, None, None

    row15 = df15.iloc[-1]
    row1h = df1h.iloc[-1]

    buy_score = 0
    sell_score = 0
    reasons = []

    # =========================
    # STRUCTURE (FIXED CONFLICTS)
    # =========================
    bos_up, bos_down = detect_structure(df15)

    if bos_up and not bos_down:
        buy_score += 10
        reasons.append("Break of Structure UP")
    elif bos_down and not bos_up:
        sell_score += 10
        reasons.append("Break of Structure DOWN")

    # =========================
    # LIQUIDITY
    # =========================
    sweep_up, sweep_down = detect_liquidity_sweep(df15)

    if sweep_up:
        sell_score += 15
        reasons.append("Liquidity Sweep UP (Fake Breakout)")
    if sweep_down:
        buy_score += 15
        reasons.append("Liquidity Sweep DOWN (Fake Breakdown)")

    # =========================
    # ORDER BLOCK
    # =========================
    bull_ob, bear_ob = detect_order_block(df15)

    if bull_ob:
        buy_score += 15
        reasons.append("Bullish Order Block")
    if bear_ob:
        sell_score += 15
        reasons.append("Bearish Order Block")

    # =========================
    # FVG
    # =========================
    bull_fvg, bear_fvg = detect_fvg(df15)

    if bull_fvg:
        buy_score += 10
        reasons.append("Bullish FVG")
    if bear_fvg:
        sell_score += 10
        reasons.append("Bearish FVG")

    # =========================
    # TREND (FIXED HIERARCHY)
    # =========================
    h1_buy = row1h["EMA20"] > row1h["EMA50"]
    m15_buy = row15["EMA20"] > row15["EMA50"]

    if h1_buy:
        buy_score += 20
        reasons.append("1H Uptrend")
    else:
        sell_score += 20
        reasons.append("1H Downtrend")

    if m15_buy:
        buy_score += 10
        reasons.append("15M Bullish")
    else:
        sell_score += 10
        reasons.append("15M Bearish")

    # =========================
    # EMA 200
    # =========================
    if row15["close"] > row15["EMA200"]:
        buy_score += 10
    else:
        sell_score += 10

    # =========================
    # MACD
    # =========================
    if row15["MACD"] > row15["MACD_SIGNAL"]:
        buy_score += 15
    else:
        sell_score += 15

    # =========================
    # RSI
    # =========================
    if row15["RSI"] < 35:
        buy_score += 10
    elif row15["RSI"] > 65:
        sell_score += 10

    # =========================
    # ADX
    # =========================
    if row15["ADX"] >= 25:
        if buy_score > sell_score:
            buy_score += 10
        else:
            sell_score += 10
        reasons.append("Strong Trend")

    # =========================
    # BOLLINGER
    # =========================
    if row15["close"] <= row15["BB_LOWER"]:
        buy_score += 5
    elif row15["close"] >= row15["BB_UPPER"]:
        sell_score += 5

    # =========================
    # SUPPORT/RESISTANCE
    # =========================
    support, resistance = get_support_resistance(df15)

    if is_breakout(df15, resistance):
        buy_score += 10
    if is_breakdown(df15, support):
        sell_score += 10

    # =========================
    # FINAL SCORE
    # =========================
    total = buy_score + sell_score

    if total == 0:
        confidence = 0
    else:
        confidence = round((max(buy_score, sell_score) / total) * 100, 2)

    signal = "BUY" if buy_score > sell_score else "SELL"

    if confidence < 60:
        signal = "HOLD"

    # =========================
    # PRICING (FIX FLOAT BUG)
    # =========================
    if signal == "HOLD":
        return signal, confidence, reasons, None, None, None

    entry = round(float(row15["close"]), 5)
    atr = float(row15["ATR"])

    if signal == "BUY":
        sl = round(entry - atr * 1.8, 5)
        tp = round(entry + atr * 3.0, 5)
    else:
        sl = round(entry + atr * 1.8, 5)
        tp = round(entry - atr * 3.0, 5)

    return signal, confidence, reasons, entry, sl, tp
