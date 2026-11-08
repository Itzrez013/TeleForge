import secrets
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OTP
from .serializers import (
    RegisterSerializer,
    VerifyOTPSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProfileSerializer,
)
from .utils import send_activation_email
from bots.serializers.bot import TelegramBotSerializer
from bots.models import TelegramBot


def _token_response(user, message):
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "message": message,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        },
        status=status.HTTP_200_OK,
    )


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():

            user = serializer.save()

            random_code = secrets.randbelow(900000) + 100000

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

    permission_classes = [AllowAny]

    def post(self, request):
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

        return _token_response(
            user,
            "Your account has been activated successfully.",
        )


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
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
                status=status.HTTP_400_BAD_REQUEST
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
                    "code": secrets.randbelow(900000) + 100000
                }
            )

            if (
                not created and
                timezone.now()
                < otp.sent_at + timedelta(seconds=60)
            ):

                return Response(
                    {
                        "message":
                        "Your account is not active. Enter the verification code already sent to your email.",
                        "verification_required": True,
                    },
                    status=status.HTTP_200_OK
                )

            random_code = secrets.randbelow(900000) + 100000

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
                    "Your account is not active. A new verification code has been sent to your email.",
                    "verification_required": True,
                },
                status=status.HTTP_200_OK
            )

        return _token_response(user, "Welcome to TeleForge.")


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["refresh"].blacklist()

        return Response(
            {"message": "Logged out successfully."},
            status=status.HTTP_200_OK,
        )


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bots = TelegramBot.objects.filter(owner=request.user)
        profile = ProfileSerializer(request.user).data
        bot_list = TelegramBotSerializer(bots,many=True).data
        return Response({"profile":profile,"user_bot_list":bot_list})