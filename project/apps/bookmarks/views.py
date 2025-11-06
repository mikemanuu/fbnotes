from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Bookmark
from .serializers import BookmarkSerializer
from apps.tags.models import Tag
from apps.notes.serializers import NoteSerializer
from apps.notes.models import Note
from django.shortcuts import get_object_or_404

class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def add_tag(self, request, pk=None):
        bookmark = self.get_object()
        name = request.data.get("name")
        if not name:
            return Response({"detail": "Tag name required"}, status=status.HTTP_400_BAD_REQUEST)
        tag, _ = Tag.objects.get_or_create(name=name.strip(), user=request.user)
        bookmark.tags.add(tag)
        return Response({"detail": "tag added"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def add_note(self, request, pk=None):
        bookmark = self.get_object()
        title = request.data.get("title")
        content = request.data.get("content")
        if not title or not content:
            return Response({"detail": "title and content required"}, status=status.HTTP_400_BAD_REQUEST)
        note = Note.objects.create(bookmark=bookmark, title=title, content=content)
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
