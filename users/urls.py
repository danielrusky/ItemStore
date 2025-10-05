from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, generate_new_password, forgot_password, EmailVerifyView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/genpassword", generate_new_password, name="generate_new_password"),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('verify_email/<str:uidb64>/<str:token>/', EmailVerifyView.as_view(), name='verify_email'),
]
