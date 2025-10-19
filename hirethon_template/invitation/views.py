from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Invitation
from .serializers import InvitationSerializer
from hirethon_template.users.models import Membership
import secrets

User = get_user_model()

class SendInvitationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InvitationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        org = serializer.validated_data["organization"]
        role = serializer.validated_data["role"]
        email = serializer.validated_data["email"]

        # Check if sender is admin
        if not Membership.objects.filter(user=request.user, organization=org, role="admin").exists():
            return Response({"error": "Only admins can invite"}, status=403)

        # Check if user already exists
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            if Membership.objects.filter(user=existing_user, organization=org).exists():
                return Response({"error": "User is already part of the organization"}, status=400)

        # Check for pending invite
        if Invitation.objects.filter(email=email, organization=org, accepted=False).exists():
            return Response({"error": "Invitation already sent"}, status=400)

        token = secrets.token_urlsafe(32)
        Invitation.objects.create(
            organization=org,
            email=email,
            role=role,
            token=token,
            invited_by=request.user
        )

        invite_link = f"https://yourdomain.com/invite/{token}"
        # TODO: send email with invite_link

        return Response({"message": "Invitation sent", "link": invite_link})


class AcceptInvitationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get("token")
        invite = get_object_or_404(Invitation, token=token, accepted=False)

        # Check if already a member
        if Membership.objects.filter(user=request.user, organization=invite.organization).exists():
            return Response({"error": "Already a member"}, status=400)

        Membership.objects.create(
            user=request.user,
            organization=invite.organization,
            role=invite.role
        )

        invite.accepted = True
        invite.save()

        return Response({"message": "Joined organization"})
    


class MyInvitationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        invites = Invitation.objects.filter(email=request.user.email, accepted=False)
        data = [
            {
                "organization": invite.organization.name,
                "role": invite.role,
                "token": invite.token,
                "invited_by": invite.invited_by.username if invite.invited_by else None,
                "created_at": invite.created_at,
            }
            for invite in invites
        ]
        return Response(data)

