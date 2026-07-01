import requests
from config import BOT_TOKEN, CHAT_ID

MESSAGE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
PHOTO_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"


def send_message(message):
    requests.post(
        MESSAGE_URL,
        json={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def format_signal(symbol, signal_data, win_rate=None):

    signal = signal_data["signal"]
    confidence = signal_data["confidence"]
    entry = signal_data.get("entry")
    sl = signal_data.get("sl")
    tp = signal_data.get("tp")
    reasons = signal_data.get("reasons", [])

    msg = f"""
🚨 TRADING SIGNAL

📊 Market: {symbol}
📈 Signal: {signal}
🎯 Confidence: {confidence:.2f}%

"""

    if entry is not None:
        msg += f"""
💰 Entry: {float(entry):.5f}
🛑 SL: {float(sl):.5f}
🏆 TP: {float(tp):.5f}

"""

    msg += f"📊 Win Rate: {win_rate if win_rate else 'N/A'}%\n\n"
    msg += "📋 Reasons:\n"

    for r in list(dict.fromkeys(reasons)):
        msg += f"• {r}\n"

    return msg


def send_signal(symbol, signal_data, win_rate=None):
    message = format_signal(symbol, signal_data, win_rate)

    requests.post(
        MESSAGE_URL,
        json={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def send_photo(photo_path, caption=""):
    with open(photo_path, "rb") as photo:
        requests.post(
            PHOTO_URL,
            data={
                "chat_id": CHAT_ID,
                "caption": caption
            },
            files={"photo": photo}
        )
