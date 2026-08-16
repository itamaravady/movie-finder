import os
import requests


DATE = "2026-08-28"
FILM_ID = "7460s2r"

CINEMA_URL = (
    "https://www.planetcinema.co.il/il/data-api-service/v1/"
    "quickbook/10100/cinema-events/in-group/"
    "planet-rishon-letziyon/with-film/"
    f"{FILM_ID}/at-date/{DATE}?attr=&lang=he_IL"
)

TICKETS_URL = (
    f"https://www.planetcinema.co.il/films/the-odyssey/{FILM_ID}"
    "#/buy-tickets-by-film?in-cinema=1072"
    f"&at={DATE}"
    f"&for-movie={FILM_ID}"
    "&view-mode=list"
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

    # Only send a Telegram message when events are found
    if event_count > 0:
        message = (
            "🎬 Planet Cinema\n"
            "Rishon LeZiyon\n"
            "The Odyssey\n"
            f"Date: {DATE}\n\n"
            f"Events found: {event_count}\n\n"
            f"🎟️ Buy tickets:\n{TICKETS_URL}"
        )

        send_telegram(message)


if __name__ == "__main__":
    main()
