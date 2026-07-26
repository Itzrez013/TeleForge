from rest_framework import serializers
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


# class ProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = [
#             "email",
#             "full_name",
#             "created_at",
#             "updated_at",
#         ]


# class ChangePasswordSerializer(serializers.Serializer):

#     old_password = serializers.CharField(
#         write_only=True
#     )

#     new_password = serializers.CharField(
#         write_only=True,
#         validators=[validate_password]
#     )