from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('register/otp/',views.VerifyOTPAPIView.as_view(),name='otp'),
    path('login/',views.LoginView.as_view(),name='login'),
]
