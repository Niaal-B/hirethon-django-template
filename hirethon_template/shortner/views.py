from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from hirethon_template.users.models import Organization, Membership
from .models import ShortURL
from django.shortcuts import get_object_or_404, redirect
from .cache import get_cached_redirect, set_cached_redirect

class CreateShortURLView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        original_url = request.data.get("original_url")
        org_slug = request.data.get("organization_slug")
        slug = request.data.get("slug")

        # Validate required fields
        if not original_url or not org_slug or not slug:
            return Response({"error": "Missing original_url, organization_slug, or slug"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate organization
        try:
            org = Organization.objects.get(slug=org_slug)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)

        # Validate membership
        membership = Membership.objects.filter(user=request.user, organization=org).first()
        if not membership:
            return Response({"error": "You are not a member of this organization"}, status=status.HTTP_403_FORBIDDEN)

        # Validate role
        if membership.role not in ["admin", "editor"]:
            return Response({"error": "You do not have permission to create short URLs"}, status=status.HTTP_403_FORBIDDEN)

        # Check slug uniqueness within org
        if ShortURL.objects.filter(organization=org, slug=slug).exists():
            return Response({"error": "Slug already in use for this organization"}, status=status.HTTP_400_BAD_REQUEST)

        # Create ShortURL
        short_url = ShortURL.objects.create(
            original_url=original_url,
            organization=org,
            created_by=request.user,
            slug=slug,
        )

        return Response({
            "id": short_url.id,
            "slug": short_url.slug,
            "short_url": f"https://yourdomain.com/{org.slug}/{short_url.slug}",
            "original_url": short_url.original_url,
            "clicks": short_url.clicks,
            "created_at": short_url.created_at,
        }, status=status.HTTP_201_CREATED)


def redirect_view(request, org_slug, slug):
    # Try Redis first
    cached_url = get_cached_redirect(org_slug, slug)
    if cached_url:
        return redirect(cached_url)

    # Fallback to DB
    org = get_object_or_404(Organization, slug=org_slug)
    short = get_object_or_404(ShortURL, organization=org, slug=slug)

    # Track click
    short.clicks += 1
    short.save()

    # Cache for future
    set_cached_redirect(org_slug, slug, short.original_url)

    return redirect(short.original_url)