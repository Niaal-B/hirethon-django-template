from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from organizations.models import Organization, Membership
from .models import ShortURL
from .serializers import ShortURLCreateSerializer

class CreateShortURLView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        original_url = request.data.get("original_url")
        org_slug = request.data.get("organization_slug")

        if not original_url or not org_slug:
            return Response({"error": "Missing original_url or organization_slug"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            org = Organization.objects.get(slug=org_slug)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)

        membership = Membership.objects.filter(user=request.user, organization=org).first()
        if not membership:
            return Response({"error": "You are not a member of this organization"}, status=status.HTTP_403_FORBIDDEN)

        if membership.role not in ["admin", "editor"]:
            return Response({"error": "You do not have permission to create short URLs"}, status=status.HTTP_403_FORBIDDEN)

        short_url = ShortURL.objects.create(
            original_url=original_url,
            organization=org,
            created_by=request.user,
        )

        return Response({
            "id": short_url.id,
            "slug": short_url.slug,
            "short_url": f"httphttp://localhost:5173/{short_url.slug}",
            "original_url": short_url.original_url,
            "clicks": short_url.clicks,
            "created_at": short_url.created_at,
        }, status=status.HTTP_201_CREATED)