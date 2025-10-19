from django.core.cache import cache

def get_cached_redirect(org_slug, slug):
    key = f"shorturl:{org_slug}:{slug}"
    return cache.get(key)

def set_cached_redirect(org_slug, slug, original_url, ttl=86400):
    key = f"shorturl:{org_slug}:{slug}"
    cache.set(key, original_url, timeout=ttl)

def delete_cached_redirect(org_slug, slug):
    key = f"shorturl:{org_slug}:{slug}"
    cache.delete(key)
