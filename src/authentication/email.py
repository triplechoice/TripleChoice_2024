from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from authentication.token import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
import os


def send_activation_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('frontend/email/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'http_protocol': os.environ.get('HTTP_PROTOCOL'),
    })
    email = EmailMessage(
        mail_subject, message, to=[user.email]
    )
    email.content_subtype = "html"
    email.send()


def send_password_reset_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Password Reset Mail.'
    message = render_to_string('frontend/email/password_reset_email.html', {
        'user': user,
        'domain': current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'http_protocol': os.environ.get('HTTP_PROTOCOL'),
    })

    email = EmailMessage(
        mail_subject, message, to=[user.email]
    )
    email.content_subtype = "html"
    email.send()

