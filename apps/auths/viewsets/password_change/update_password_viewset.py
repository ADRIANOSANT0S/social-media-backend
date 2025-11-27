from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auths.serializers.password_change import UpdatePasswordSerializer


class UpdatePasswordView(APIView):
    """Handle password update requests after the user has verified the temporary code."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                user = serializer.save()

                language = request.META.get("HTTP_ACCEPT_LANGUAGE", "en").split(",")[0][
                    :2
                ]
                context = {
                    "user": user,
                    "user_agent_line": request.META.get("HTTP_USER_AGENT", "").split(
                        " "
                    ),
                }

                with translation.override(language):
                    html_content = render_to_string(
                        "email/password_changed_notification.html", context
                    )

                email = EmailMultiAlternatives(
                    subject=_("Your password was changed."),
                    body=_(
                        "Your password was changed. If this was not you, please contact us."
                    ),
                    from_email="Social Media X <email@test.com>",
                    to=[user.email],
                )
                email.attach_alternative(html_content, "text/html")

                email.send()

        except Exception as e:
            return Response(
                {"detail": f"Could not update password: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"detail": "Password updated successfully."},
            status=status.HTTP_200_OK,
        )
