from django.db import models
from bookmarks.models import Bookmark
from django.conf import settings

class Note(models.Model):
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.content[:120]
