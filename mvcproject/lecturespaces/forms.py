from django import forms
from .models import Lecturespace

class LecturespaceForm(forms.ModelForm):
    class Meta:
        model = Lecturespace
        fields = ['title', 'youtube_url', 'tags']
