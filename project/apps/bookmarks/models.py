from django.db import models
from django.conf import settings
import hashlib
from apps.tags.models import Tag

def compute_url_hash(url: str) -> str:
    return hashlib.sha256(url.encode('utf-8')).hexdigest()

class Bookmark(models.Model):
    VISIBILITY_CHOICES = [('private','private'),('public','public')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    url = models.URLField(max_length=1000)
    url_hash = models.CharField(max_length=64, db_index=True)
    title = models.CharField(max_length=500, blank=True)
    excerpt = models.TextField(blank=True)
    source = models.CharField(max_length=50, default='facebook')
    saved_at = models.DateTimeField(null=True, blank=True)
    metadata_fetched = models.BooleanField(default=False)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='private')
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, through='BookmarkTag', related_name='bookmarks')

    class Meta:
        indexes = [
            models.Index(fields=['user','created_at']),
        ]
        unique_together = ('user','url_hash')

    def save(self, *args, **kwargs):
        if not self.url_hash:
            self.url_hash = compute_url_hash(self.url)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or self.url[:80]

class BookmarkTag(models.Model):
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('bookmark','tag')

class Media(models.Model):
    MEDIA_TYPES = [('image','image'),('video','video'),('other','other')]
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE, related_name='media')
    media_url = models.URLField(max_length=2000)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, default='image')
    thumbnail_url = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.media_url[:80]
