from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        if request.user.is_authenticated:
            return Response({"Error":"شما الانشم لاگینی"})