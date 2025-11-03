from rest_framework import serializers
from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','user','name','slug','created_at']
        read_only_fields = ['user','slug','created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return Tag.objects.create(user=user, **validated_data)
