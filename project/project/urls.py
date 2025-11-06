from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/bookmarks/", include("apps.bookmarks.urls")),
    path("api/notes/", include("apps.notes.urls")),
    path("api/tags/", include("apps.tags.urls")),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/audit/", include("apps.audit.urls")),

    # DRF browsable auth (session login)
    path("api-auth/", include("rest_framework.urls")),
]
