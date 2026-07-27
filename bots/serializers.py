from rest_framework import serializers

class BotTokenSerializer(serializers.Serializer):
    token = serializers.CharField()