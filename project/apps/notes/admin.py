from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "bookmark", "title", "created_at", "content")
    list_filter = ('user',)
    search_fields = ("title", "content")
