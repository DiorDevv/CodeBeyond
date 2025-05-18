from django.core.mail import send_mail

from core.settings import EMAIL_HOST_USER


def send_verifications(email, message, subject=None):
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [email],
    )
