from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from hirethon_template.users.models import Organization, Membership
from .serializers import OrganizationCreateSerializer
from django.utils.text import slugify

class CreateOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)

        slug = slugify(name)
        if Organization.objects.filter(slug=slug).exists():
            return Response({'error': 'Organization with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)

        org = Organization.objects.create(name=name, slug=slug, created_by=request.user)
        Membership.objects.create(user=request.user, organization=org, role='admin')

        return Response({
            'id': org.id,
            'name': org.name,
            'slug': org.slug,
            'role': 'admin',
            'joined_at': org.created_at,
        }, status=status.HTTP_201_CREATED)


class MemberOrganizationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        memberships = Membership.objects.filter(user=request.user).exclude(role='admin')
        data = [
            {
                'id': m.organization.id,
                'name': m.organization.name,
                'slug': m.organization.slug,
                'role': m.role,
                'joined_at': m.joined_at,
            }
            for m in memberships
        ]
        return Response({'organizations': data}, status=status.HTTP_200_OK)