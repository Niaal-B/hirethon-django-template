from django.db import models
from django.conf import settings
from hirethon_template.users.models import Organization
from django.utils.crypto import get_random_string

class ShortURL(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_url = models.URLField()
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_random_string(length=6)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug} → {self.original_url}"