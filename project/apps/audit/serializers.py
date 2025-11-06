from rest_framework import serializers
from .models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ["id", "user", "action", "timestamp", "bookmark"]
        read_only_fields = ["id", "timestamp", "user"]
