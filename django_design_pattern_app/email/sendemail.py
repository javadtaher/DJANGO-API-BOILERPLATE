from django.core.mail import EmailMultiAlternatives
from django_design_pattern.settings import base


class Send_Email:
    def __init__(self, to, subject: str = None, body: str = None, from_email=base.EMAIL_HOST_USER):
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email=from_email,
            to=[to]
        )
        content = body
        msg.attach_alternative(f'<h3>Hi</h3><p>{content}</p>', "text/html")
        msg.send()
