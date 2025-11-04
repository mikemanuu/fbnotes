from rest_framework import serializers
from .models import Bookmark, Media
from apps.notes.serializers import NoteSerializer
from apps.tags.serializers import TagSerializer
from apps.notes.models import Note
from django.db import transaction

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id','media_url','media_type','thumbnail_url']

class BookmarkCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    notes = serializers.ListField(child=serializers.CharField(), required=False)
    class Meta:
        model = Bookmark
        fields = ['id','url','title','excerpt','visibility','tags','notes']

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        notes = validated_data.pop('notes', [])
        user = self.context['request'].user
        normalized_url = validated_data.get('url')
        from .models import compute_url_hash
        url_hash = compute_url_hash(normalized_url)
        if Bookmark.objects.filter(user=user, url_hash=url_hash).exists():
            raise serializers.ValidationError("Bookmark with this URL already exists")
        with transaction.atomic():
            bookmark = Bookmark.objects.create(user=user, url=normalized_url, url_hash=url_hash, **validated_data)
            from tags.models import Tag
            for t in tags:
                tag_obj, _ = Tag.objects.get_or_create(user=user, name=t, defaults={'slug': t.lower().replace(' ','-')})
                bookmark.tags.add(tag_obj)
            for n in notes:
                Note.objects.create(bookmark=bookmark, author=user, content=n)
            from .tasks import fetch_metadata
            fetch_metadata.delay(bookmark.id)
        return bookmark

class BookmarkSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)
    notes = NoteSerializer(many=True, read_only=True)
    class Meta:
        model = Bookmark
        fields = ['id','url','title','excerpt','visibility','created_at','saved_at','metadata_fetched','tags','media','notes']
