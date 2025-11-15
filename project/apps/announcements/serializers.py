from rest_framework import serializers
from .models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    class Meta:
        model = Announcement
        fields = ["id","title","body","pinned","author","created_at","publish_at","is_public"]

    def get_author(self, obj):
        if obj.author:
            return {"id": obj.author.id, "username": getattr(obj.author, "username", None)}
        return None
