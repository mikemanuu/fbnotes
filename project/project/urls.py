from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/bookmarks/", include("apps.bookmarks.urls")),
    path("api/notes/", include("apps.notes.urls")),
    path("api/tags/", include("apps.tags.urls")),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/audit/", include("apps.audit.urls")),

    # DRF browsable auth (session login)
    path("api-auth/", include("rest_framework.urls")),

    # openAPI schema and UIs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
