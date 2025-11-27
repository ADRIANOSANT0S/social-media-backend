from django.urls import path

from apps.auths.viewsets import (
    LoginAPIView,
    LogoutAPIView,
    PasswordCodeVerifyView,
    PasswordVerifyEmailView,
    RefreshTokenAPIView,
    RequestRecoverEmailCodeViewset,
    UpdateEmailViewSet,
    UpdatePasswordView,
    VerifyUserCredentialsViewSet,
)

# router = DefaultRouter()
# router.register(r'login', LoginAPIView, basename="auth-login")

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="auth-login"),
    path("logout/", LogoutAPIView.as_view(), name="auth-logout"),
    path("refresh-token/", RefreshTokenAPIView.as_view(), name="refresh-token"),
    path(
        "email/verify-code/",
        RequestRecoverEmailCodeViewset.as_view(),
        name="verify-recover-email-code",
    ),
    path(
        "email/verify-credentials/",
        VerifyUserCredentialsViewSet.as_view(),
        name="verify-user-credentials",
    ),
    path(
        "email/update-email/",
        UpdateEmailViewSet.as_view(),
        name="update-email",
    ),
    path(
        "password/verify-email/",
        PasswordVerifyEmailView.as_view(),
        name="password-verify-email",
    ),
    path(
        "password/verify-code/",
        PasswordCodeVerifyView.as_view(),
        name="password-code-verify",
    ),
    path(
        "password/update-password/",
        UpdatePasswordView.as_view(),
        name="update-password",
    ),
]
