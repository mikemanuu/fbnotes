from rest_framework import serializers
from .models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ["id", "user", "action", "created_at", "target_model"]
        read_only_fields = ["id", "created_at", "user"]
