from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ActivateAccountView,
    ForgotPasswordView,
    ResetPasswordConfirmView,
    EditProfileView,
)


urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path(
        "auth/activate/<uid>/<token>/", ActivateAccountView.as_view(), name="activate"
    ),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("me/", EditProfileView.as_view(), name="edit-profile"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path(
        "password-reset-confirm/<uid>/<token>/",
        ResetPasswordConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]
