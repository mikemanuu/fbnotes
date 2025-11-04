from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.notes.models import Note
from apps.bookmarks.models import Bookmark
from apps.audit.models import AuditLog
from apps.notes.serializers import NoteSerializer


# --------------------------------------------------------------------
# REST API Views
# --------------------------------------------------------------------

class NoteListCreateAPIView(generics.ListCreateAPIView):
    """
    List all notes or create a new note.
    Accessible via: /api/notes/
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(bookmark__user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        bookmark_id = self.request.data.get('bookmark_id')
        bookmark = get_object_or_404(Bookmark, id=bookmark_id, user=self.request.user)
        note = serializer.save(bookmark=bookmark)
        
        # Log the action
        AuditLog.objects.create(
            user=self.request.user,
            action=f"Created a note for bookmark '{bookmark.post_title}'",
            ip_address=self.request.META.get('REMOTE_ADDR')
        )
        return note


class NoteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a note.
    Accessible via: /api/notes/<id>/
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(bookmark__user=self.request.user)

    def perform_update(self, serializer):
        note = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action=f"Updated note ID {note.id}",
            ip_address=self.request.META.get('REMOTE_ADDR')
        )

    def perform_destroy(self, instance):
        AuditLog.objects.create(
            user=self.request.user,
            action=f"Deleted note ID {instance.id}",
            ip_address=self.request.META.get('REMOTE_ADDR')
        )
        instance.delete()


# --------------------------------------------------------------------
# Template Views (For Web Interface)
# --------------------------------------------------------------------

@method_decorator(login_required, name='dispatch')
class NoteDashboardView(APIView):
    """
    Render the user's note dashboard (HTML).
    """
    def get(self, request):
        notes = Note.objects.filter(bookmark__user=request.user).select_related('bookmark')
        return render(request, 'notes/dashboard.html', {'notes': notes})


@login_required
def create_note_view(request, bookmark_id):
    """
    Create a note from a form submission.
    """
    bookmark = get_object_or_404(Bookmark, id=bookmark_id, user=request.user)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            note = Note.objects.create(bookmark=bookmark, content=content)
            AuditLog.objects.create(
                user=request.user,
                action=f"Created a note via web for bookmark '{bookmark.post_title}'",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return redirect('notes:dashboard')

    return render(request, 'notes/create_note.html', {'bookmark': bookmark})


@login_required
def delete_note_view(request, note_id):
    """
    Delete a note from the web interface.
    """
    note = get_object_or_404(Note, id=note_id, bookmark__user=request.user)

    if request.method == 'POST':
        AuditLog.objects.create(
            user=request.user,
            action=f"Deleted note via web (ID: {note.id})",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        note.delete()
        return redirect('notes:dashboard')

    return render(request, 'notes/confirm_delete.html', {'note': note})
