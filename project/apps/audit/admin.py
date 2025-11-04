from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id','action','target_model','target_id','user','created_at')
    readonly_fields = ('user','action','target_model','target_id','meta','created_at')
