from django.contrib.auth.views import PasswordResetView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView
from .serializers import CustomRegisterSerializer, CustomLoginSerializer
from rest_framework import status, response, generics
from authentication import tasks
from authentication import models, serializers

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    # def perform_create(self, serializer):
    #     user = serializer.save(self.request)
    #     verifier = user_verification.UserVerifier(user=user)
    #     token = verifier.generate_token()
    #     verifier.send_token_to_mail(token, purpose="verification")


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = validated_data["user"]
        response_data = {
            "user": {"email": user.email, "full_name": user.full_name},
            "access_token": validated_data["access"],
            "refresh_token": validated_data["refresh"],
        }
        return response.Response(response_data, status=status.HTTP_200_OK)


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.user_cache
        tasks.send_password_reset_email(user.id)
        return response

class GetUserByView(generics.RetrieveAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserDetailsSerializer