from support_resistance import (
    get_support_resistance,
    is_breakout,
    is_breakdown
)

from market_structure import detect_structure
from liquidity import detect_liquidity_sweep
from smart_money import detect_order_block, detect_fvg
from news_filter import is_high_impact_news_time


def generate_signal(df15, df1h):

    # =========================
    # NEWS FILTER
    # =========================

    news_block, _ = is_high_impact_news_time()

    if news_block:
        return "HOLD", 0, ["High impact news detected"], None, None, None

    row15 = df15.iloc[-1]
    row1h = df1h.iloc[-1]

    buy_score = 0
    sell_score = 0
    reasons = []

    # =========================
    # MARKET STRUCTURE (BOS)
    # =========================

    bos_up, bos_down = detect_structure(df15)

    if bos_up:
        buy_score += 10
        reasons.append("Break of Structure UP")

    if bos_down:
        sell_score += 10
        reasons.append("Break of Structure DOWN")

    # =========================
    # LIQUIDITY SWEEP FILTER
    # =========================

    sweep_up, sweep_down = detect_liquidity_sweep(df15)

    if sweep_up:
        sell_score += 15
        reasons.append("Liquidity Sweep UP (Fake Breakout)")

    if sweep_down:
        buy_score += 15
        reasons.append("Liquidity Sweep DOWN (Fake Breakdown)")

    # =========================
    # ORDER BLOCKS
    # =========================

    bull_ob, bear_ob = detect_order_block(df15)

    if bull_ob:
        buy_score += 15
        reasons.append("Bullish Order Block")

    if bear_ob:
        sell_score += 15
        reasons.append("Bearish Order Block")

    # =========================
    # FAIR VALUE GAP (FVG)
    # =========================

    bull_fvg, bear_fvg = detect_fvg(df15)

    if bull_fvg:
        buy_score += 10
        reasons.append("Bullish FVG")

    if bear_fvg:
        sell_score += 10
        reasons.append("Bearish FVG")

    # =========================
    # 1H TREND
    # =========================

    if row1h["EMA20"] > row1h["EMA50"]:
        buy_score += 20
        reasons.append("1H Uptrend")
    else:
        sell_score += 20
        reasons.append("1H Downtrend")

    # =========================
    # 15M TREND
    # =========================

    if row15["EMA20"] > row15["EMA50"]:
        buy_score += 20
        reasons.append("15M Bullish")
    else:
        sell_score += 20
        reasons.append("15M Bearish")

    # =========================
    # EMA200 FILTER
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
    # ADX FILTER
    # =========================

    if row15["ADX"] >= 25:
        if buy_score > sell_score:
            buy_score += 10
        else:
            sell_score += 10

        reasons.append("Strong Trend")

    # =========================
    # BOLLINGER BANDS
    # =========================

    if row15["close"] <= row15["BB_LOWER"]:
        buy_score += 5
    elif row15["close"] >= row15["BB_UPPER"]:
        sell_score += 5

    # =========================
    # SUPPORT / RESISTANCE
    # =========================

    support, resistance = get_support_resistance(df15)

    if is_breakout(df15, resistance):
        buy_score += 10

    if is_breakdown(df15, support):
        sell_score += 10

    # =========================
    # FINAL DECISION
    # =========================

    confidence = (buy_score + sell_score) / 2

    if buy_score > sell_score:
        signal = "BUY"
    elif sell_score > buy_score:
        signal = "SELL"
    else:
        signal = "HOLD"

    if confidence < 60:
        signal = "HOLD"

    # =========================
    # RISK MANAGEMENT
    # =========================

    if signal == "HOLD":
        return signal, 0, reasons, None, None, None

    entry = round(row15["close"], 2)
    atr = row15["ATR"]

    if signal == "BUY":
        sl = round(entry - atr * 1.5, 2)
        tp = round(entry + atr * 3, 2)
    else:
        sl = round(entry + atr * 1.5, 2)
        tp = round(entry - atr * 3, 2)

    return signal, confidence, reasons, entry, sl, tp