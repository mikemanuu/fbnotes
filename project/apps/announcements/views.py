from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Announcement
from .serializers import AnnouncementSerializer

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_public=True).order_by("-pinned","-created_at")
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  
    