from django.urls import path
from . import views

app_name = 'bots'

urlpatterns = [
    path('get-token/',views.GetTokenView.as_view(),name='get_token'),
    path('bots/<int:bot_id>/deactivate/',views.BotDeactivateView.as_view(),name='bot_deactivate'),
    path('bots/<int:bot_id>/',views.BotDetailView.as_view(),name='bots'),
    path('bots/<int:bot_id>/commands/<int:command_id>/',views.BotCommandDetailView.as_view(),name='bot_commands'),
    path('bots/<int:bot_id>/commands/<int:command_id>/responses/<int:response_id>/',views.CommandResponseDetailView.as_view(),name='command_responses'),
]
