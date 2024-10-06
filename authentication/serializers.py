from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from dj_rest_auth import serializers as rest_auth_serializers
from authentication.models import CustomUser


User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["email"] = self.validated_data.get("email", "")
        data["full_name"] = self.validated_data.get("full_name", "")
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email exists")
        return value


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        credentials = {
            "email": attrs.get("email"),
            "password": attrs.get("password"),
        }

        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials."
                )
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        refresh = TokenObtainPairSerializer.get_token(user)
        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)
        attrs["user"] = user
        return attrs


class CustomUserDetailsSerializer(rest_auth_serializers.UserDetailsSerializer):
    class Meta:
        fields = "__all__"
        model = CustomUser