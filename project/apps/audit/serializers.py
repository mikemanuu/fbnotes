from rest_framework import serializers
from .models import AuditLog
from apps.accounts.serializers import UserSerializer  

class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "action",
            "target_model",
            "target_id",
            "meta",
            "created_at",  
            "user",
        ]

    def get_user(self, obj):
        try:
            u = obj.user
            return {"id": u.id, "username": getattr(u, "username", None)}
        except Exception:
            return None
