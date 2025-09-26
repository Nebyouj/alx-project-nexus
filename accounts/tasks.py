
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email(subject, message, recipient):
    if isinstance(recipient, list):
        recipient = recipient[0]
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )
