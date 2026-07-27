from rest_framework import serializers
from ..models import CommandResponse

class TelegramBotCommandResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandResponse
        fields = ["command","text","created_at","updated_at"]