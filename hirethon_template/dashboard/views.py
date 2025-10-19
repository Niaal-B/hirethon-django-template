from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from hirethon_template.users.models import Membership

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        memberships = Membership.objects.filter(user=user).select_related('organization')

        orgs = [
            {
                "id": m.organization.id,
                "name": m.organization.name,
                "slug": m.organization.slug,
                "role": m.role,
                "joined_at": m.joined_at,
            }
            for m in memberships
        ]

        return Response({
            "message": f"Welcome {user.name}, this is your dashboard.",
            "email": user.email,
            "user_id": user.id,
            "organizations": orgs,
        })
