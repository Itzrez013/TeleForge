from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import Notification,Security_and_Privacy
from .serializers import NotificationSerializer,Security_and_PrivacySerializer

# Create your views here.


class NotificationsView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class SecurityandPrivacyView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Security_and_Privacy.objects.all()
    serializer_class = Security_and_PrivacySerializer