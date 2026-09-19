import os
import requests

# -----------------------------
# GET SECRETS
# -----------------------------

API_KEY = os.environ.get("OPENWEATHER_API_KEY")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


# -----------------------------
# OPENWEATHER
# -----------------------------

URL = "https://api.openweathermap.org/data/2.5/forecast"

parameters = {
    "lat": 22.769129,
    "lon": 86.214905,
    "appid": API_KEY,
    "cnt": 4
}

response = requests.get(URL, params=parameters)
response.raise_for_status()

data = response.json()


# -----------------------------
# CHECK FOR RAIN
# -----------------------------

will_rain = False

for forecast in data["list"]:
    condition_code = forecast["weather"][0]["id"]

    print("Weather ID:", condition_code)

    if condition_code < 700:
        will_rain = True
        break


# -----------------------------
# SEND TELEGRAM
# -----------------------------

if will_rain:

    telegram_url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    telegram_parameters = {
        "chat_id": CHAT_ID,
        "text": "☔ Rain expected in the next 12 hours. Take an umbrella!"
    }

    telegram_response = requests.post(
        telegram_url,
        data=telegram_parameters
    )

    telegram_response.raise_for_status()

    print("Telegram message sent!")

else:
    print("No rain expected.")