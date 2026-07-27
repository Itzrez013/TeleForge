from django.urls import path
from . import views

app_name = 'bots'

urlpatterns = [
    path('get-token/',views.GetTokenView.as_view(),name='get_token'),
    path('bot/<int:bot_id>/',views.BotDetailViews.as_view(),name='bots'),
    path('bot<int:bot_id>/commands/<int:command_id>/',views.BotCommandDetailView.as_view(),name='bot_commands'),
]
