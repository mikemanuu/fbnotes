from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.accounts.urls')),
    path('api/v1/', include('apps.bookmarks.urls')),
    path('api/v1/', include('apps.notes.urls')),
    path('api/v1/', include('apps.tags.urls')),
    path('api/v1/', include('apps.audit.urls')),
    path('', TemplateView.as_view(template_name='dashboard.html'), name='home'),
]
