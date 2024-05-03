import random

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from reviews.models import User


def generate_confirmation_code(username):
    user = get_object_or_404(User, username=username)
    confirmation_code = ''.join(
        random.choices(settings.CONF_GEN, k=15)
    )
    user.confirmation_code = confirmation_code
    user.save()

    send_mail(
        subject=settings.MAIL_SUBJECT,
        message=confirmation_code,
        from_email=settings.EMAIL_CONFIRM,
        recipient_list=[user.email],
        fail_silently=False,
    )
