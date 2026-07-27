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