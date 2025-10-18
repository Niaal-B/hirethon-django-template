from django.contrib.auth import get_user_model
from celery import shared_task
from config import celery_app
from django.core.mail import send_mail

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()



@shared_task
def send_verification_email_task(email, verify_url):
    subject = "Verify your email"
    message = f"Click the link to verify your account: {verify_url}"
    send_mail(
        subject=subject,
        message=message,
        from_email="noreply@hirethon.local",
        recipient_list=[email],
        fail_silently=False,
    )
