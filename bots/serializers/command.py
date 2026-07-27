from rest_framework import serializers
from ..models import BotCommand
import re

class TelegramBotCommandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotCommand
        fields = ["bot","name","name","description","created_at","updated_at"]


class AddCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotCommand
        fields = [
            "name",
            "description",
        ]


    def validate_name(self, value):

        value = value.strip().lower()

        if not value.startswith("/"):
            raise serializers.ValidationError(
                "Commands must start with '/'."
            )

        if len(value) > 32:
            raise serializers.ValidationError(
                "Commands cannot be longer than 32 characters."
            )

        if " " in value:
            raise serializers.ValidationError(
                "Commands cannot contain spaces."
            )

        if not re.match(r"^/[a-z0-9_]+$", value):
            raise serializers.ValidationError(
                "Only lowercase letters, numbers and '_' are allowed."
            )

        bot = self.context.get("bot")

        if bot and BotCommand.objects.filter(
                bot=bot,
                name=value
        ).exists():

            raise serializers.ValidationError(
                "This command already exists for this bot."
            )

        return value


    def validate_description(self, value):

        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError(
                "Description must contain at least 5 characters."
            )

        return value