from django.urls import path
from .views import CreateOrganizationView,MemberOrganizationsView

urlpatterns = [
path("create/", CreateOrganizationView.as_view(), name="create-organization"),
path("memberships/", MemberOrganizationsView.as_view(), name="member-organizations"),

]
