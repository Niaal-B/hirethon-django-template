from django.urls import path
from .views import SendInvitationView, AcceptInvitationView,MyInvitationsView

urlpatterns = [
    path("send/", SendInvitationView.as_view(), name="send-invite"),
    path("accept/", AcceptInvitationView.as_view(), name="accept-invite"),
    path("my/", MyInvitationsView.as_view(), name="my-invitations"),
]
