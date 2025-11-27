from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


def send_user_email(user, subject, template_name, context):
    """
    Envia email usando templates HTML, com suporte a i18n.
    """
    # Renderiza o HTML
    html_content = render_to_string(template_name, context)

    # Cria email
    email = EmailMultiAlternatives(
        subject=_(subject),
        body=_(subject),  # fallback para texto
        from_email="Your App <noreply@yourapp.com>",
        to=[user.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
