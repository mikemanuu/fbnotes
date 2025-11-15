from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from datetime import datetime, timedelta
from apps.notes.models import Note
from apps.bookmarks.models import Bookmark
from apps.tags.models import Tag

class MetricsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes_count = Note.objects.count()
        bookmarks_count = Bookmark.objects.count()
        categories_count = Tag.objects.count()
        latest_note = Note.objects.order_by("-updated_at").first() if hasattr(Note, "updated_at") else None
        latest_bookmark = Bookmark.objects.order_by("-updated_at").first() if hasattr(Bookmark, "updated_at") else None
        last_synced = None
        if latest_note and latest_bookmark:
            last = max(latest_note.updated_at, latest_bookmark.updated_at)
            last_synced = last.isoformat()
        elif latest_note:
            last_synced = latest_note.updated_at.isoformat()
        elif latest_bookmark:
            last_synced = latest_bookmark.updated_at.isoformat()

        data = {
            "notes_count": notes_count,
            "bookmarks_count": bookmarks_count,
            "categories_count": categories_count,
            "last_synced": last_synced,
        }
        return Response(data)


class Last7DaysAPIView(APIView):
    """
    Return labels and data for the last 7 days for notes/bookmarks.
    path param `model` = 'notes' | 'bookmarks'
    """
    permission_classes = [IsAuthenticated]

    def get_queryset_counts(self, model_class):
        # returns list of counts for the last 7 days (starting 6 days ago .. today)
        today = datetime.utcnow().date()
        labels = []
        counts = []
        for days_back in range(6, -1, -1):
            d = today - timedelta(days=days_back)
            labels.append(d.strftime("%a"))
            start = datetime.combine(d, datetime.min.time())
            end = datetime.combine(d, datetime.max.time())
            q = model_class.objects.filter(created_at__range=(start, end)).count()
            counts.append(q)
        return labels, counts

    def get(self, request, model_name):
        model_map = {
            "notes": Note,
            "bookmarks": Bookmark
        }
        model_class = model_map.get(model_name)
        if not model_class:
            return Response({"detail": "Invalid model"}, status=400)
        labels, data = self.get_queryset_counts(model_class)
        return Response({"labels": labels, "data": data})
