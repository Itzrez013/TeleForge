from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "password",
        ]


    def validate_full_name(self, value):

        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Full name must contain at least 3 characters."
            )

        return value


    def create(self, validated_data):

        return User.objects.create_user(
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            password=validated_data["password"],
        )


class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()
    code = serializers.IntegerField(min_value=100000,max_value=999999)


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True
    )


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField(write_only=True)

    def validate_refresh(self, value):
        try:
            refresh_token = RefreshToken(value)
        except TokenError as exc:
            raise serializers.ValidationError(
                "Invalid or expired refresh token."
            ) from exc

        request_user_id = str(self.context["request"].user.pk)
        if str(refresh_token["user_id"]) != request_user_id:
            raise serializers.ValidationError(
                "Refresh token does not belong to the authenticated user."
            )

        return refresh_token


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "created_at",
        ]


# class ChangePasswordSerializer(serializers.Serializer):

#     old_password = serializers.CharField(
#         write_only=True
#     )

#     new_password = serializers.CharField(
#         write_only=True,
#         validators=[validate_password]
#     )