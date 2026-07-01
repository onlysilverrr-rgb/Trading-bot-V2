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


def send_photo(photo_path, caption=""):

    with open(photo_path, "rb") as photo:

        requests.post(

            PHOTO_URL,

            data={
                "chat_id": CHAT_ID,
                "caption": caption
            },

            files={
                "photo": photo
            }

        )
