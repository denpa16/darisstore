from django.core.mail import EmailMultiAlternatives, get_connection

from config import settings


def send_mail(subject, message, email: str, html_message=None):
    connection = get_connection(
        backend=settings.EMAIL_BACKEND,
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_ssl=False,
    )
    mail = EmailMultiAlternatives(
        connection=connection,
        subject=subject,
        from_email=settings.SERVER_EMAIL,
        body=message,
        to=[email],
    )
    if html_message:
        mail.attach_alternative(html_message, "text/html")

    return mail.send()
