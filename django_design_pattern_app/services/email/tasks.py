from django.core.mail import EmailMultiAlternatives
from django_design_pattern.celery import app
from django_design_pattern.settings import base


@app.task
def send_email_task(to, subject, body):
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=base.EMAIL_HOST_USER,
        to=[to]
    )
    content = body
    msg.attach_alternative(f'<h3>Hi</h3><p>{content}</p>', "text/html")
    msg.send()