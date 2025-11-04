from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    ACTION_CHOICES = [('CREATE','CREATE'),('UPDATE','UPDATE'),('DELETE','DELETE')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=100, choices=ACTION_CHOICES)
    target_model = models.CharField(max_length=100)
    target_id = models.IntegerField(null=True, blank=True)
    meta = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.action} {self.target_model} {self.target_id} by {self.user}"
