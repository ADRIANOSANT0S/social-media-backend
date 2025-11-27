from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.core.services.code_service import CodeService
from apps.users.models import User

from ..serializers import UserRegisterSerializer


class UserRegisterViewSet(ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        """View that create a new user."""

        serializer = UserRegisterSerializer(data=request.data)

        # Valid that the user input data is valid.
        serializer.is_valid(raise_exception=True)

        user = User(**serializer.validated_data)

        # Generate code for the user can change account email.
        code = CodeService(user).set_code()
        user.recover_email_code = make_password(code)

        # Get user language.
        language = request.META.get("HTTP_ACCEPT_LANGUAGE", "en").split(",")[0][:2]

        # preparar contexto do email
        context = {
            "user": user,
            "code": code,
            "user_agent_line": request.META.get("HTTP_USER_AGENT", "").split(" "),
        }

        # renderizar email no idioma correto
        with translation.override(language):
            html_content = render_to_string(
                "emails/welcome_with_email_code.html", context
            )

        #  Try send email for the user.
        try:
            email = EmailMultiAlternatives(
                subject=_("Your email change code"),
                body=_("Use this code to change your email."),
                from_email="Your App <noreply@dominio.com>",
                to=[user.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
        except Exception:
            return Response(
                {"error": "Could not send email. Please try again later."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save use in data base
        user.save()

        return Response(
            {"details": "Account created successfully."}, status=status.HTTP_201_CREATED
        )
