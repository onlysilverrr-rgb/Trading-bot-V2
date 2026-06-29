import time
import schedule

from config import MARKETS, ENTRY_TIMEFRAME, TREND_TIMEFRAME
from data import get_market_data
from indicators import add_indicators
from patterns import detect_patterns
from strategy import generate_signal
from telegram_bot import send_message
from logger import log_trade
from performance import update_trade_result, get_win_rate


# =========================
# MEMORY (prevent duplicate signals)
# =========================
last_signal = {}


def scan_market():

    print("\n" + "=" * 50)
    print("📊 Scanning Markets...")
    print("=" * 50)

    win_rate = get_win_rate()

    for market in MARKETS:

        try:

            print(f"\n📊 Scanning {market}...")

            # =========================
            # DATA
            # =========================

            data15 = get_market_data(market, ENTRY_TIMEFRAME)
            data1h = get_market_data(market, TREND_TIMEFRAME)

            if not data15 or not data1h:
                print("❌ No data")
                continue

            # =========================
            # INDICATORS
            # =========================

            df15 = add_indicators(data15)
            df1h = add_indicators(data1h)

            if df15 is None or df1h is None:
                print("❌ Indicator error")
                continue

            df15 = detect_patterns(df15)
            df1h = detect_patterns(df1h)

            # =========================
            # SIGNAL
            # =========================

            signal, confidence, reasons, entry, sl, tp = generate_signal(df15, df1h)

            print(f"Signal: {signal} | Confidence: {confidence}%")
            print(f"Reasons: {reasons}")

            # =========================
            # DUPLICATE FILTER
            # =========================

            if market in last_signal and last_signal[market] == signal:
                print("🔁 Duplicate signal skipped")
                continue

            last_signal[market] = signal

            # =========================
            # TRADE LOGIC
            # =========================

            if signal != "HOLD":

                log_trade(market, signal, confidence, entry, sl, tp)

                # ⚠️ PERFORMANCE UPDATE (TEMP: assumes win=False placeholder)
                # You can upgrade this later with real TP/SL hit tracking
                update_trade_result(win=True)

                message = f"""
🚨 TRADING SIGNAL

📊 Market: {market}
📈 Signal: {signal}
🎯 Confidence: {confidence}%

💰 Entry: {entry}
🛑 SL: {sl}
🏆 TP: {tp}

📊 Win Rate: {win_rate}%

📋 Reasons:
"""

                for r in reasons:
                    message += f"• {r}\n"

                send_message(message)

                print("✅ Telegram sent")

            else:
                print("❌ Signal filtered")

        except Exception as e:
            print(f"❌ Error scanning {market}")
            print(e)


# =========================
# START
# =========================
scan_market()

schedule.every(15).minutes.do(scan_market)

print("\n🤖 Bot Running on Railway...")
print("⏰ Scanning every 15 minutes")

while True:
    schedule.run_pending()
    time.sleep(1)