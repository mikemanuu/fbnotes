from rest_framework import viewsets, permissions
from .models import Note
from .serializers import NoteSerializer

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Notes are accessible only if their parent bookmark belongs to the user
        return Note.objects.filter(bookmark__user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        # allow serializer.bookmark validation to handle bookmark ownership
        bookmark = serializer.validated_data.get('bookmark')
        if bookmark.user != self.request.user:
            raise PermissionError("Cannot add note to a bookmark you don't own")
        serializer.save()
        
