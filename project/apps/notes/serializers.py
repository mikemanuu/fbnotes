from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Note
        fields = ['id','bookmark','author','content','pinned','created_at','updated_at']
        read_only_fields = ['author','created_at','updated_at']


