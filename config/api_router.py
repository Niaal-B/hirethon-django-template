from django.urls import include, path
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from hirethon_template.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/", include("hirethon_template.dashboard.api.urls")),
    path("organizations/", include("hirethon_template.Organization.urls")),
]
