from django.urls import path
from . import views

app_name = 'general'

urlpatterns = [
    path('notification/',views.NotificationsView.as_view(),name='notification'),
]