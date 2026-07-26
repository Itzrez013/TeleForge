from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from datetime import timedelta
from django.utils import timezone
from .serializers import RegisterSerializer,VerifyOTPSerializer
from random import randint
from .models import User,OTP
from .utils import send_activation_email

# Create your views here.

class RegisterAPIView(APIView):

    def post(self, request):
        if request.user.is_authenticated:
            return Response({"Error":"لاگینی که همین الانشم کجا میخوای بری"})
        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

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

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class VerifyOTPAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return Response({"Error":"لاگینی که همین الانشم کجا میخوای بری"})
        serializer = VerifyOTPSerializer(
            data=request.data
        )

        if serializer.is_valid():

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

            user.is_active = True
            user.save()

            otp.delete()

            return Response(
                {
                    "message": "Your account has been activated successfully."
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )