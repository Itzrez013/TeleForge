from django.shortcuts import render,get_object_or_404
from accounts.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializers import BotTokenSerializer,TelegramBotSerializer,TelegramBotCommandsSerializer,TelegramBotCommandResponseSerializer,AddCommandSerializer
from .utils import get_bot_information
from .models import TelegramBot,CommandResponse,BotCommand


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


class BotDetailViews(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,bot_id):
        bot = get_object_or_404(TelegramBot,id=bot_id,owner=request.user)
        commands = bot.commands.all()
        return Response({"bot":TelegramBotSerializer(bot).data,
                        "commands":TelegramBotCommandsSerializer(commands,many=True).data})
    # def post(self,request,bot_id):
    #     bot = get_object_or_404(TelegramBot,id=bot_id,owner=request.user)



class BotCommandDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,bot_id,command_id):
        command = get_object_or_404(BotCommand,id=command_id,bot__id=bot_id,bot__owner=request.user)
        responses = command.responses.all()
        return Response({"command":TelegramBotCommandsSerializer(command).data,
                            "command_responses":TelegramBotCommandResponseSerializer(responses,many=True).data})