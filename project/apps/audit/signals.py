from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AuditLog
from bookmarks.models import Bookmark
from notes.models import Note
from tags.models import Tag

def log_action(user, action, instance, **kwargs):
    AuditLog.objects.create(
        user=user if getattr(user, 'is_authenticated', False) else None,
        action=action,
        target_model=instance.__class__.__name__,
        target_id=getattr(instance, 'id', None),
        meta={}
    )

@receiver(post_save, sender=Bookmark)
def bookmark_saved(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    user = getattr(instance, 'user', None)
    log_action(user, action, instance)

@receiver(post_delete, sender=Bookmark)
def bookmark_deleted(sender, instance, **kwargs):
    user = getattr(instance, 'user', None)
    log_action(user, 'DELETE', instance)

@receiver(post_save, sender=Note)
def note_saved(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    log_action(instance.author, action, instance)

@receiver(post_delete, sender=Note)
def note_deleted(sender, instance, **kwargs):
    log_action(instance.author, 'DELETE', instance)

@receiver(post_save, sender=Tag)
def tag_saved(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    log_action(instance.user, action, instance)
