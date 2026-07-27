from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers.bot import (BotTokenSerializer,TelegramBotSerializer,UpdateBotSerializer)
from .serializers.command import (TelegramBotCommandsSerializer,AddCommandSerializer,UpdateCommandSerializer)
from .serializers.response import (TelegramBotCommandResponseSerializer,AddResponseSerializer)

from .utils import get_bot_information
from .models import TelegramBot, CommandResponse, BotCommand


class BaseBotMixin:

    def get_bot(self, bot_id):

        return get_object_or_404(
            TelegramBot,
            id=bot_id,
            owner=self.request.user
        )

    def get_command(self, bot_id, command_id):

        return get_object_or_404(
            BotCommand,
            id=command_id,
            bot__id=bot_id,
            bot__owner=self.request.user
        )

    def get_response(self, bot_id, command_id, response_id):

        return get_object_or_404(
            CommandResponse,
            id=response_id,
            command__id=command_id,
            command__bot__id=bot_id,
            command__bot__owner=self.request.user
        )


class GetTokenView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = BotTokenSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        token = serializer.validated_data["token"]

        data = get_bot_information(token)

        if not data:

            return Response(
                {
                    "error": "Invalid token."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        bot_id = data["id"]
        username = data["username"]
        name = data["first_name"]

        bot = TelegramBot.objects.filter(
            bot_id=bot_id
        ).first()

        if bot and bot.owner == request.user:

            return Response(
                {
                    "error":
                    "You have already added this bot."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if bot:

            return Response(
                {
                    "error":
                    "This bot belongs to another user."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        bot = TelegramBot.objects.create(

            owner=request.user,
            token=token,
            bot_id=bot_id,
            username=username,
            name=name

        )

        return Response(
            {
                "message": "Bot added successfully.",
                "bot_id": bot.id
            },
            status=status.HTTP_201_CREATED
        )


class BotDetailView(BaseBotMixin,APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, bot_id):

        bot = self.get_bot(bot_id)

        commands = bot.commands.all()

        return Response(
            {
                "bot":
                TelegramBotSerializer(bot).data,

                "commands":
                TelegramBotCommandsSerializer(
                    commands,
                    many=True
                ).data
            }
        )

    def post(self, request, bot_id):

        bot = self.get_bot(bot_id)

        serializer = AddCommandSerializer(
            data=request.data,
            context={
                "bot": bot
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            bot=bot
        )

        return Response(
            {
                "message":
                "Bot command created successfully."
            },
            status=status.HTTP_201_CREATED
        )

    def patch(self,request,bot_id):

        bot = self.get_bot(bot_id)

        serializer = UpdateBotSerializer(

            bot,

            data=request.data,

            partial=True

        )

        serializer.is_valid(
            raise_exception=True
        )

        bot = serializer.save()


        return Response(

            {
                "message":
                "Bot updated successfully.",

                "bot":
                TelegramBotSerializer(
                    bot
                ).data
            },

            status=status.HTTP_200_OK

        )

class BotCommandDetailView(BaseBotMixin,APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, bot_id, command_id):

        command = self.get_command(
            bot_id,
            command_id
        )

        responses = command.responses.all()

        return Response(
            {
                "command":
                TelegramBotCommandsSerializer(
                    command
                ).data,

                "command_responses":
                TelegramBotCommandResponseSerializer(
                    responses,
                    many=True
                ).data
            }
        )

    def post(self, request, bot_id, command_id):

        command = self.get_command(
            bot_id,
            command_id
        )

        serializer = AddResponseSerializer(

            data=request.data,

            context={
                "command": command
            }

        )

        serializer.is_valid(
            raise_exception=True
        )

        response = serializer.save(
            command=command
        )

        return Response(

            {
                "message":
                "Response created successfully.",

                "response":
                TelegramBotCommandResponseSerializer(
                    response
                ).data
            },

            status=status.HTTP_201_CREATED

        )


    def patch(self, request, bot_id, command_id):

        command = self.get_command(
            bot_id,
            command_id
        )

        serializer = UpdateCommandSerializer(

            command,

            data=request.data,

            partial=True,

            context={
                "bot": command.bot
            }

        )

        serializer.is_valid(
            raise_exception=True
        )

        command = serializer.save()

        return Response(

            {
                "message":
                "Command updated successfully.",

                "command":
                TelegramBotCommandsSerializer(
                    command
                ).data
            },

            status=status.HTTP_200_OK

        )