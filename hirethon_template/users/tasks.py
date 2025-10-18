from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_verification_email_task(email, verify_url):
    subject = "Verify your Hirethon account"
    message = f"Click the link to verify your account:\n\n{verify_url}"
    send_mail(
        subject=subject,
        message=message,
        from_email="noreply@hirethon.local",
        recipient_list=[email],
        fail_silently=False,
    )
