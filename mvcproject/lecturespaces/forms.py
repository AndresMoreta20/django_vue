from django import forms
from .models import Lecturespace
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re

class LecturespaceForm(forms.ModelForm):
    """
    Form for creating Lecturespaces, where users only input the YouTube URL.
    """
    class Meta:
        model = Lecturespace
        fields = ['youtube_url']  # Include only the YouTube URL field
        widgets = {
            'youtube_url': forms.URLInput(attrs={'placeholder': 'Enter YouTube URL here'}),
        }

    def clean_youtube_url(self):
        youtube_url = self.cleaned_data.get('youtube_url')
        # Add custom validation logic for youtube_url, e.g., check URL format
        # Example: Validate if it's a proper YouTube URL
        if not self.is_valid_youtube_url(youtube_url):
            raise forms.ValidationError("Please enter a valid YouTube URL.")
        return youtube_url

    @staticmethod
    def is_valid_youtube_url(url):
        # Regular expression for validating a YouTube URL
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        return re.match(youtube_regex, url) is not None

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']