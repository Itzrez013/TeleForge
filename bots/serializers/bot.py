from rest_framework import serializers
from ..models import TelegramBot

class BotTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

class TelegramBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramBot
        fields = ["bot_id",
                  "username",
                  "name",
                  "is_acrive",
                  "created_at",
                  "updated_at"]

class UpdateBotSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelegramBot
        fields = [
            "name",
            "is_active",
        ]


    def validate_name(self, value):

        value = value.strip()

        if len(value) < 3:

            raise serializers.ValidationError(
                "Bot name must contain at least 3 characters."
            )

        if len(value) > 100:

            raise serializers.ValidationError(
                "Bot name cannot be longer than 100 characters."
            )

        return value