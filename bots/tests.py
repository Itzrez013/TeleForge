from unittest.mock import patch
from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import BotCommand, CommandResponse, TelegramBot


class TelegramBotFlowTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="bot-owner@example.com",
            full_name="Bot Owner",
            password="SecurePassword123!",
        )
        self.bot = TelegramBot.objects.create(
            owner=self.user,
            token="123456:bot-token",
            bot_id=123456,
            username="example_bot",
            name="Example Bot",
        )
        self.command = BotCommand.objects.create(
            bot=self.bot,
            name="/hello",
            description="Say hello",
        )

    def test_webhook_sends_the_command_response(self):
        CommandResponse.objects.create(
            command=self.command,
            text="Hello there",
        )

        with patch("bots.views.send_message") as send_message:
            response = self.client.post(
                reverse("bots:telegram_webhook"),
                {
                    "message": {
                        "text": "/hello@example_bot extra text",
                        "chat": {"id": 42},
                    }
                },
                format="json",
                HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN=self.bot.webhook_secret,
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        send_message.assert_called_once_with(self.bot, 42, "Hello there")

    def test_webhook_ignores_commands_for_another_bot(self):
        CommandResponse.objects.create(
            command=self.command,
            text="Hello there",
        )

        with patch("bots.views.send_message") as send_message:
            response = self.client.post(
                reverse("bots:telegram_webhook"),
                {
                    "message": {
                        "text": "/hello@some_other_bot",
                        "chat": {"id": 42},
                    }
                },
                format="json",
                HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN=self.bot.webhook_secret,
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        send_message.assert_not_called()

    def test_configured_webhook_url_resolves_to_webhook_view(self):
        resolved = resolve(urlparse(settings.WEBHOOK_URL).path)

        self.assertEqual(resolved.url_name, "telegram_webhook")

    def test_bot_name_can_be_updated(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            reverse("bots:bots", args=[self.bot.pk]),
            {"name": "Renamed Bot"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.bot.refresh_from_db()
        self.assertEqual(self.bot.name, "Renamed Bot")

    def test_command_cannot_have_a_second_response(self):
        CommandResponse.objects.create(
            command=self.command,
            text="Original response",
        )
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse(
                "bots:bot_commands",
                args=[self.bot.pk, self.command.pk],
            ),
            {"text": "Replacement response"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            CommandResponse.objects.filter(command=self.command).count(),
            1,
        )

    def test_deactivation_failure_returns_gateway_error(self):
        self.client.force_authenticate(self.user)

        with patch("bots.views.deactivate_bot", return_value=False):
            response = self.client.post(
                reverse("bots:bot_deactivate", args=[self.bot.pk]),
                format="json",
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_502_BAD_GATEWAY,
        )
