import requests

from config import BOT_TOKEN, CHAT_ID
from strategy import format_signal


MESSAGE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
PHOTO_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"


# =========================
# BASIC TEXT MESSAGE (RAW)
# =========================
def send_message(message):
    requests.post(
        MESSAGE_URL,
        json={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
    )


# =========================
# SIGNAL MESSAGE (MAIN FIX)
# =========================
def send_signal(symbol, signal_data, win_rate=None):

    message = format_signal(symbol, signal_data, win_rate)

    requests.post(
        MESSAGE_URL,
        json={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
    )


# =========================
# PHOTO SENDER (UNCHANGED)
# =========================
def send_photo(photo_path, caption=""):

    with open(photo_path, "rb") as photo:

        requests.post(
            PHOTO_URL,
            data={
                "chat_id": CHAT_ID,
                "caption": caption,
                "parse_mode": "HTML"
            },
            files={
                "photo": photo
            }
        )
