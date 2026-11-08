import requests


def get_bot_information(token):

    url = f"https://api.telegram.org/bot{token}/getMe"

    response = requests.get(url, timeout=10)

    data = response.json()

    if not data["ok"]:
        return None

    return data["result"]