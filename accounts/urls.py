from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('register/otp/',views.VerifyOTPAPIView.as_view(),name='otp'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path("Dashboaed/",views.DashboardView.as_view(),name='dashboard'),
]