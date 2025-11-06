from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["bookmark", "title", "content"]
        widgets = {"content": forms.Textarea(attrs={"rows": 6})}
