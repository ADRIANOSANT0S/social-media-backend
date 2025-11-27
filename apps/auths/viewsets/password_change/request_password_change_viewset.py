from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auths.serializers.password_change import PasswordVerifyEmailSerializer
from apps.auths.services import PasswordChangeService


class PasswordVerifyEmailView(APIView):
    """
    Handle requests to request a password reset code via email.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordVerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.context["user"]

        service = PasswordChangeService(user=user)
        service.verify_email(serializer.validated_data["email"])

        code_data = service.get_code_from_redis()
        code = code_data["code"]

        language = request.META.get("HTTP_ACCEPT_LANGUAGE", "en").split(",")[0][:2]

        context = {
            "user": user,
            "code": code,
            "user_agent_line": request.META.get("HTTP_USER_AGENT", "").split(" "),
        }

        with translation.override(language):
            html_content = render_to_string("emails/password_reset_code.html", context)

        email_message = EmailMultiAlternatives(
            subject=_("Your password reset code"),
            body=_("Use this code to reset your password."),
            from_email="Your App <noreply@dominio.com>",
            to=[user.email],
        )
        email_message.attach_alternative(html_content, "text/html")

        try:
            email_message.send()
        except Exception:
            return Response(
                {"error": _("Could not send email. Please try again later.")},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"detail": _("Password reset code sent successfully.")},
            status=status.HTTP_200_OK,
        )
