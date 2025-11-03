from celery import shared_task
import requests
from bs4 import BeautifulSoup
from .models import Bookmark, Media

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def fetch_metadata(self, bookmark_id):
    try:
        bookmark = Bookmark.objects.get(id=bookmark_id)
    except Bookmark.DoesNotExist:
        return
    try:
        resp = requests.get(bookmark.url, timeout=10, headers={'User-Agent':'fb-notes-bot/1.0'})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        og_title = soup.find('meta', property='og:title')
        og_desc = soup.find('meta', property='og:description')
        og_image = soup.find('meta', property='og:image')
        if og_title and og_title.get('content'):
            bookmark.title = bookmark.title or og_title['content'][:500]
        if og_desc and og_desc.get('content'):
            bookmark.excerpt = bookmark.excerpt or og_desc['content'][:2000]
        if og_image and og_image.get('content'):
            Media.objects.update_or_create(bookmark=bookmark, media_url=og_image['content'], defaults={'media_type':'image'})
        bookmark.metadata_fetched = True
        bookmark.save()
    except Exception as exc:
        raise self.retry(exc=exc)
