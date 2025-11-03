from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('bookmarks.urls')),
    path('api/v1/', include('notes.urls')),
    path('api/v1/', include('tags.urls')),
    path('api/v1/', include('audit.urls')),
    path('', TemplateView.as_view(template_name='dashboard.html'), name='home'),
]
