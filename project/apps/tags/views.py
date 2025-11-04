from rest_framework import viewsets, permissions
from .models import Tag
from .serializers import TagSerializer

class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage tags.
    Only authenticated users can access their own tags.
    """
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only tags for the logged-in user
        return Tag.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user on creation
        serializer.save(user=self.request.user)
