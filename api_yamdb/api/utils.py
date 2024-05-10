import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from api.constants import EMAIL_CONFIRM, EMAIL_SUBJECT

User = get_user_model()


def generate_confirmation_code(username):
    user = get_object_or_404(User, username=username)
    confirmation_code = str(uuid.uuid4())[:15]
    user.confirmation_code = confirmation_code
    user.save()

    send_mail(
        subject=EMAIL_SUBJECT,
        message=confirmation_code,
        from_email=EMAIL_CONFIRM,
        recipient_list=[user.email],
        fail_silently=False,
    )
