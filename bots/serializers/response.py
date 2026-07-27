from rest_framework import serializers
from ..models import CommandResponse

class TelegramBotCommandResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandResponse
        fields = ["command","text","created_at","updated_at"]


class AddResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommandResponse
        fields = [
            "text",
        ]


    def validate_text(self, value):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "Response text cannot be empty."
            )

        if len(value) < 1:

            raise serializers.ValidationError(
                "Response text is too short."
            )

        if len(value) > 4096:

            raise serializers.ValidationError(
                "Response text cannot exceed 4096 characters."
            )

        return value