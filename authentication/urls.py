from .views import CustomRegisterView, CustomLoginView, LogoutView
from django.urls import path


urlpatterns = [
    # path("register/", RegisterView.as_view(), name="rest_register"),
    path('register/', CustomRegisterView.as_view(), name='custom_register'),
    path("login/", CustomLoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    # path("user/", UserDetailsView.as_view(), name="rest_user_details"),
]