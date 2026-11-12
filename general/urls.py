from django.urls import path
from . import views

app_name = 'general'

urlpatterns = [
    path('notification/',views.NotificationsView.as_view(),name='notification'),
    path('security_and_privacy/',views.SecurityandPrivacyView.as_view(),name='SecurityandPrivacy'),
]