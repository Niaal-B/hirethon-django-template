from django.utils.crypto import get_random_string

def generate_unique_slug(org):
    for _ in range(5):  
        slug = get_random_string(length=6)
        if not ShortURL.objects.filter(organization=org, slug=slug).exists():
            return slug
    raise Exception("Could not generate unique slug for organization")
