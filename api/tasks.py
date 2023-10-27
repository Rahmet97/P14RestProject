import logging

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(email, title, description):
    logging.info(f'Title >>>> {title}')
    send_mail(
        subject=title,
        from_email='From 127.0.0.1',
        recipient_list=[email],
        message=description,
        fail_silently=True
    )
    return 'Done'
