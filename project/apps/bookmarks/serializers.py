from rest_framework import serializers
from .models import Bookmark
from apps.tags.serializers import TagSerializer
from apps.notes.serializers import NoteSerializer

class BookmarkSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    notes = NoteSerializer(many=True, read_only=True, source="note_set")

    class Meta:
        model = Bookmark
        fields = [
            "id", "title", "url", "user", "created_at", "updated_at",
            "tags", "notes"
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        validated_data["user"] = user
        return super().create(validated_data)
