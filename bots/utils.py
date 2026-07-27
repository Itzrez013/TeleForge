import requests


def get_bot_information(token):

    url = f"https://api.telegram.org/bot{token}/getMe"

    response = requests.get(url)

    data = response.json()

    if not data["ok"]:
        return None

    return data["result"]