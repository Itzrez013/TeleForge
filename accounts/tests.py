from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTP


class JWTAuthenticationTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            full_name="Test User",
            password="SecurePassword123!",
        )
        self.user.is_active = True
        self.user.save(update_fields=["is_active"])

    def test_login_returns_jwt_pair_without_session_cookie(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "email": self.user.email,
                "password": "SecurePassword123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertNotIn("sessionid", response.cookies)

    def test_otp_activation_returns_jwt_pair(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])
        OTP.objects.create(user=self.user, code=123456)

        response = self.client.post(
            reverse("accounts:otp"),
            {"email": self.user.email, "code": 123456},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertTrue(get_user_model().objects.get(pk=self.user.pk).is_active)

    def test_dashboard_requires_and_accepts_bearer_access_token(self):
        dashboard_url = reverse("accounts:dashboard")
        self.assertEqual(
            self.client.get(dashboard_url).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(dashboard_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_rotates_and_blacklists_the_previous_token(self):
        refresh = str(RefreshToken.for_user(self.user))

        response = self.client.post(
            reverse("accounts:token_refresh"),
            {"refresh": refresh},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertNotEqual(response.data["refresh"], refresh)

        old_token_response = self.client.post(
            reverse("accounts:token_refresh"),
            {"refresh": refresh},
            format="json",
        )
        self.assertEqual(
            old_token_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        rotated_token_response = self.client.post(
            reverse("accounts:token_refresh"),
            {"refresh": response.data["refresh"]},
            format="json",
        )
        self.assertEqual(
            rotated_token_response.status_code,
            status.HTTP_200_OK,
        )

    def test_logout_blacklists_only_the_authenticated_users_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)
        other_user = get_user_model().objects.create_user(
            email="other@example.com",
            full_name="Other User",
            password="SecurePassword123!",
        )
        other_user.is_active = True
        other_user.save(update_fields=["is_active"])
        other_refresh = str(RefreshToken.for_user(other_user))
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        rejected_response = self.client.post(
            reverse("accounts:logout"),
            {"refresh": other_refresh},
            format="json",
        )
        self.assertEqual(
            rejected_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        response = self.client.post(
            reverse("accounts:logout"),
            {"refresh": str(refresh)},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        refresh_response = self.client.post(
            reverse("accounts:token_refresh"),
            {"refresh": str(refresh)},
            format="json",
        )
        self.assertEqual(
            refresh_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    @patch("accounts.views.send_activation_email")
    def test_inactive_login_still_sends_otp_instead_of_tokens(self, send_email):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])

        response = self.client.post(
            reverse("accounts:login"),
            {
                "email": self.user.email,
                "password": "SecurePassword123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("access", response.data)
        send_email.assert_called_once()
