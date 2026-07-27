from django.urls import path
from . import views

app_name = 'bots'

urlpatterns = [
    path('get-token/',views.GetTokenView.as_view(),name='get_token'),
]
