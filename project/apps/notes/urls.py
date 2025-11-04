from django.urls import path
from .views import NoteListCreateAPIView, NoteDetailAPIView, NoteDashboardView, create_note_view, delete_note_view

app_name = 'notes'

urlpatterns = [
    path('api/notes/', NoteListCreateAPIView.as_view(), name='note-list-create'),
    path('api/notes/<int:pk>/', NoteDetailAPIView.as_view(), name='note-detail'),
    path('dashboard/', NoteDashboardView.as_view(), name='dashboard'),
    path('create/<int:bookmark_id>/', create_note_view, name='create-note'),
    path('delete/<int:note_id>/', delete_note_view, name='delete-note'),
]
