from django.core.mail import send_mail
from config.celery import app


@app.task()
def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        'ranizomiddin@gmail.com',
        recipient_list
    )
