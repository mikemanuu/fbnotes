from django.contrib import admin
from .models import Bookmark, Media, BookmarkTag

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id','user','title','url','metadata_fetched','created_at')
    search_fields = ('title','url','excerpt')
    list_filter = ('metadata_fetched','visibility')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id','media_url','media_type','bookmark')
