from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auths.serializers.email_change import UpdateEmailSerializer
from apps.core.services import CodeService
from apps.users.models import User


class UpdateEmailViewSet(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        user = self._get_user_from_flow(request)
        serializer = UpdateEmailSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)

        new_code = CodeService(user).set_code()

        language = request.META.get("HTTP_ACCEPT_LANGUAGE", "en").split(",")[0][:2]

        context = {
            "user": user,
            "code": new_code,
            "user_agent_line": request.META.get("HTTP_USER_AGENT", "").split(" "),
        }

        with translation.override(language):
            html_content = render_to_string(
                "emails/email_changed_notification.html", context
            )

        email = EmailMultiAlternatives(
            subject=_("Your email change code"),
            body=_("Use this code to change your email."),
            from_email="Your App <noreply@dominio.com>",
            to=[user.email],
        )

        email.attach_alternative(html_content, "text/html")

        try:
            email.send()
            user.recover_email_code = make_password(new_code)
            user.save()

        except Exception:
            print("Error sending email")
            return Response(
                {"error": "Could not send email. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"detail": _("Update email successfully.")},
            status=status.HTTP_200_OK,
        )

    def _get_user_from_flow(self, request):
        user_id = request.data.get("user_id")
        return get_object_or_404(User, id=user_id)
