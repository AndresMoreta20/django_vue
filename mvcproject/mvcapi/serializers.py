from rest_framework import serializers
from .models import Lecturespace, Flashcard, Tag
from .models import StudySession

class StudySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySession
        fields = '__all__'

class LecturespaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturespace
        fields = '__all__'

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']
