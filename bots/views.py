from django.shortcuts import render,get_object_or_404
from accounts.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializers import BotTokenSerializer
from .utils import get_bot_information
from .models import TelegramBot


# Create your views here.


class GetTokenView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = BotTokenSerializer(data=requests.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        data = get_bot_information(token)
        if not data:
            return Response(
                {
                    "error":"Invalid token."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        bot_id = data["id"]

        username = data["username"]

        name = data["first_name"]
        bot = TelegramBot.objects.filter(bot_id=bot_id).first()
        if bot:
            if bot.owner == request.user:

                return Response(
                    {
                        "error":
                        "You have already added this bot."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )


            return Response(
                {
                    "error":
                    "This bot belongs to another user."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        TelegramBot.objects.create(

            owner=request.user,

            token=token,

            bot_id=bot_id,

            username=username,

            name=name

        )

