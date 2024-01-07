from django.contrib import admin
from .models import Tag, Lecturespace, Flashcard, UserSavedLecturespace, UserSavedFlashcard

admin.site.register(Tag)
admin.site.register(Lecturespace)
admin.site.register(Flashcard)
admin.site.register(UserSavedLecturespace)
admin.site.register(UserSavedFlashcard)
