from rest_framework import serializers
from .models import TelegramBot,BotCommand,CommandResponse

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

class TelegramBotCommandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotCommand
        fields = ["bot","name","name","description","created_at","updated_at"]

class TelegramBotCommandResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandResponse
        fields = ["command","text","created_at","updated_at"]


class AddCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotCommand
        fields = ["bot","name","description"]