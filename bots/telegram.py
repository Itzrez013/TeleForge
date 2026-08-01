import requests


BASE_URL = "https://api.telegram.org/bot"


def make_request(
        token,
        method,
        data=None
):

    response = requests.post(

        f"{BASE_URL}{token}/{method}",

        json=data

    )

    if response.status_code != 200:
        return None

    data = response.json()

    if not data.get("ok"):
        return None

    return data.get("result")


# ----------------------------------------
# General
# ----------------------------------------

def get_me(token):

    return make_request(
        token,
        "getMe"
    )


# ----------------------------------------
# Commands
# ----------------------------------------

def build_commands(bot):

    commands = []

    for command in bot.commands.all():

        commands.append(
            {
                "command":
                command.name.replace("/", ""),

                "description":
                command.description
            }
        )

    return commands


def set_commands(bot):

    return make_request(

        bot.token,

        "setMyCommands",

        {
            "commands":
            build_commands(bot)
        }

    )


def delete_commands(bot):

    return make_request(

        bot.token,

        "deleteMyCommands"

    )


def get_commands(bot):

    return make_request(

        bot.token,

        "getMyCommands"

    )


# ----------------------------------------
# Webhook
# ----------------------------------------

def set_webhook(
        bot,
        webhook_url
):

    return make_request(

        bot.token,

        "setWebhook",

        {
            "url": webhook_url,
            "secret_token": bot.webhook_secret,
        }

    )


def delete_webhook(bot):

    return make_request(

        bot.token,

        "deleteWebhook"

    )


def get_webhook_info(bot):

    return make_request(

        bot.token,

        "getWebhookInfo"

    )


# ----------------------------------------
# Messaging
# ----------------------------------------

def send_message(
        bot,
        chat_id,
        text
):

    return make_request(

        bot.token,

        "sendMessage",

        {
            "chat_id":
            chat_id,

            "text":
            text
        }

    )


# ----------------------------------------
# Updates
# ----------------------------------------

def get_updates(bot):

    return make_request(

        bot.token,

        "getUpdates"

    )


# ----------------------------------------
# Sync
# ----------------------------------------

def sync_bot(
        bot,
        webhook_url
):

    if not delete_commands(bot):
        return False

    if not set_commands(bot):
        return False

    if not delete_webhook(bot):
        return False

    if not set_webhook(
            bot,
            webhook_url
    ):
        return False

    bot.needs_sync = False

    bot.save(
        update_fields=[
            "needs_sync"
        ]
    )

    return True


# ----------------------------------------
# Activation
# ----------------------------------------

def activate_bot(
        bot,
        webhook_url
):

    return sync_bot(
        bot,
        webhook_url
    )


def deactivate_bot(bot):

    if not delete_commands(bot):
        return False

    if not delete_webhook(bot):
        return False

    return True