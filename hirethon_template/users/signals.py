from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from hirethon_template.users.models import User, Organization, Membership

@receiver(post_save, sender=User)
def create_org_and_membership(sender, instance, created, **kwargs):
    if created:
        org_name = instance.name or instance.email.split('@')[0]
        org_slug = slugify(org_name)

        org = Organization.objects.create(
            name=org_name,
            slug=org_slug,
            created_by=instance
        )

        Membership.objects.create(
            user=instance,
            organization=org,
            role='admin'
        )
