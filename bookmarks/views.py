from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Bookmark
from .serializers import BookmarkSerializer, BookmarkCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

class BookmarkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title','excerpt','notes__content']
    filterset_fields = ['visibility','archived']

    def get_serializer_class(self):
        if self.action in ['create']:
            return BookmarkCreateSerializer
        return BookmarkSerializer

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user, archived=False).prefetch_related('tags','media','notes').order_by('-created_at')

    def perform_destroy(self, instance):
        instance.archived = True
        instance.save()

    @action(detail=True, methods=['post'])
    def export(self, request, pk=None):
        bookmark = self.get_object()
        data = BookmarkSerializer(bookmark).data
        return Response(data)
