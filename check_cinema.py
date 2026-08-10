import os
import requests


CINEMA_URL = (
    "https://www.planetcinema.co.il/il/data-api-service/v1/"
    "quickbook/10100/cinema-events/in-group/"
    "planet-rishon-letziyon/with-film/7460s2r/"
    "at-date/2026-08-21?attr=&lang=he_IL"
)

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def get_events():
    response = requests.get(CINEMA_URL, timeout=30)
    response.raise_for_status()

    data = response.json()
    return data["body"]["events"]


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
        },
        timeout=30,
    )

    response.raise_for_status()


def main():
    events = get_events()
    event_count = len(events)

    message = (
        "🎬 Planet Cinema\n"
        "Rishon LeZiyon\n"
        "Film: 7460s2r\n"
        "Date: 2026-08-21\n\n"
        f"Events found: {event_count}"
    )

    send_telegram(message)


if __name__ == "__main__":
    main()
