from random import randint
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import User, OTP
from .serializers import (
    RegisterSerializer,
    VerifyOTPSerializer,
    LoginSerializer,ProfileSerializer
)
from .utils import send_activation_email
from bots.serializers import TelegramBotSerializer
from bots.models import TelegramBot

class RegisterView(APIView):

    def post(self, request):

        if request.user.is_authenticated:
            return Response(
                {
                    "error": "You are already logged in."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():

            user = serializer.save()

            random_code = randint(
                100000,
                999999
            )

            OTP.objects.update_or_create(
                user=user,
                defaults={
                    "code": random_code,
                }
            )

        send_activation_email(
            email=user.email,
            random_code=random_code,
            subject="TeleForge Verification Code"
        )

        return Response(
            {
                "message":
                "Verification code has been sent successfully."
            },
            status=status.HTTP_201_CREATED
        )


class VerifyOTPAPIView(APIView):

    def post(self, request):

        if request.user.is_authenticated:
            return Response(
                {
                    "error": "You are already logged in."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = VerifyOTPSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User does not exist."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            otp = OTP.objects.get(user=user)

        except OTP.DoesNotExist:

            return Response(
                {
                    "error": "OTP code does not exist."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if timezone.now() > otp.sent_at + timedelta(minutes=5):

            otp.delete()

            return Response(
                {
                    "error": "OTP code has expired."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp.code != code:

            return Response(
                {
                    "error": "OTP code is incorrect."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            user.is_active = True
            user.save()

            otp.delete()

        login(request, user)

        return Response(
            {
                "message":
                "Your account has been activated successfully."
            },
            status=status.HTTP_200_OK
        )


class LoginView(APIView):

    def post(self, request):

        if request.user.is_authenticated:
            return Response(
                {
                    "error": "You are already logged in."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = LoginSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:

            return Response(
                {
                    "error":
                    "Email or password is incorrect."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not user.check_password(password):

            return Response(
                {
                    "error":
                    "Email or password is incorrect."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.is_active:

            otp, created = OTP.objects.get_or_create(
                user=user,
                defaults={
                    "code": randint(
                        100000,
                        999999
                    )
                }
            )

            if (
                not created and
                timezone.now()
                < otp.sent_at + timedelta(seconds=60)
            ):

                return Response(
                    {
                        "error":
                        "Please wait 60 seconds before requesting another code."
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

            random_code = randint(
                100000,
                999999
            )

            otp.code = random_code
            otp.save()

            send_activation_email(
                email=user.email,
                random_code=random_code,
                subject="TeleForge Verification Code"
            )

            return Response(
                {
                    "message":
                    "Your account is not active. A new verification code has been sent to your email."
                },
                status=status.HTTP_200_OK
            )

        login(request, user)

        return Response(
            {
                "message":
                "Welcome to TeleForge."
            },
            status=status.HTTP_200_OK
        )


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        bots = TelegramBot.objects.filter(owner=request.user)
        profile = ProfileSerializer(request.user).data
        bot_list = TelegramBotSerializer(bots,many=True).data
        return Response({"profile":profile,"user_bot_list":bot_list})