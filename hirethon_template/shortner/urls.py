from django.urls import path
from .views import redirect_view,CreateShortURLView,ListShortURLsView,DeleteShortURLView,ResolveShortURLView

urlpatterns = [
    path("create/", CreateShortURLView.as_view(), name="create-short-url"),
    path("list/", ListShortURLsView.as_view(), name="list-short-urls"),
    path("delete/<int:pk>/", DeleteShortURLView.as_view(), name="delete-short-url"),
    path("<slug:org_slug>/<str:slug>/", redirect_view, name="redirect"),
    path("resolve/", ResolveShortURLView.as_view(), name="resolve-short-url"),
]