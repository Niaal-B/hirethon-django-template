from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from hirethon_template.users.tasks import send_verification_email_task

def send_verification_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    frontend_url = f"http://localhost:5173/verify-email?uid={uid}&token={token}"

    send_verification_email_task.delay(user.email, frontend_url)
