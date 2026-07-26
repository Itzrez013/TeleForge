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