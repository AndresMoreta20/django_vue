from django.db import models
from django.conf import settings

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Lecturespace(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class Flashcard(models.Model):
    title = models.CharField(max_length=200, default='Default Title')
    content = models.TextField()
    lecturespace = models.ForeignKey(Lecturespace, on_delete=models.CASCADE, related_name='flashcards')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Flashcard for {self.lecturespace.title}"

class UserSavedLecturespace(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lecturespace = models.ForeignKey(Lecturespace, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'lecturespace')

class UserSavedFlashcard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'flashcard')

class FlashcardVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE, related_name='votes')
    like = models.BooleanField()  # True for like, False for dislike

    class Meta:
        unique_together = ('user', 'flashcard')