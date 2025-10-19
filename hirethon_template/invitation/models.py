from django.db import models
from hirethon_template.users.models import Organization
from django.contrib.auth import get_user_model

User = get_user_model()

class Invitation(models.Model):
    ROLE_CHOICES = [
    ("admin", "Admin"),
    ("editor", "Editor"),
    ("viewer", "Viewer"),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    token = models.CharField(max_length=64, unique=True)
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
