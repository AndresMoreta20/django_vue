from django.shortcuts import get_object_or_404
from rest_framework import generics, views, status
from rest_framework.response import Response
from lecturespaces.models import Lecturespace, Flashcard, Tag
from .models import StudySession
from .serializers import LecturespaceSerializer, FlashcardSerializer, TagSerializer, StudySessionSerializer
import random


# List Views for Lecturespaces, Flashcards, and Tags
class LecturespaceList(generics.ListAPIView):
    queryset = Lecturespace.objects.all()
    serializer_class = LecturespaceSerializer

class FlashcardList(generics.ListAPIView):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer

class TagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

# Start a study session based on a tag and get the first flashcard
class StartStudySession(views.APIView):
    def post(self, request):
        tag_name = request.data.get('tag_name')
        tag = get_object_or_404(Tag, name=tag_name)
        flashcards = Flashcard.objects.filter(lecturespace__tags=tag)
        if flashcards.exists():
            selected_flashcard = random.choice(flashcards)
            session = StudySession.objects.create(total_flashcards=flashcards.count())
            return Response({
                'session_id': session.id,
                'flashcard': FlashcardSerializer(selected_flashcard).data
            })
        else:
            return Response({'error': 'No flashcards available for this tag'}, status=status.HTTP_404_NOT_FOUND)

# Provide feedback for a flashcard in a study session
class FlashcardFeedback(views.APIView):
    def post(self, request, session_id):
        session = get_object_or_404(StudySession, id=session_id)
        remembered = request.data.get('remembered', False)

        if remembered:
            session.remembered += 1
        else:
            session.forgotten += 1

        session.save()

        # Logic to get the next flashcard
        tag = session.tag
        flashcards = Flashcard.objects.filter(lecturespace__tags=tag).exclude(id=request.data.get('flashcard_id'))
        if flashcards.exists():
            next_flashcard = random.choice(flashcards)
            return Response(FlashcardSerializer(next_flashcard).data)
        else:
            return Response({'message': 'No more flashcards in this session'}, status=status.HTTP_200_OK)

class EndStudySession(views.APIView):
    def post(self, request, session_id):
        # Fetch the study session using the session_id
        study_session = get_object_or_404(StudySession, id=session_id)

        # Calculate the session summary
        total_flashcards = study_session.total_flashcards
        remembered = study_session.remembered
        forgotten = study_session.forgotten

        # Generate suggestions (this can be more sophisticated based on your application's logic)
        suggestions = []
        if remembered < forgotten:
            suggestions.append("Review the session again for better retention.")
        else:
            suggestions.append("Great job! Consider revising occasionally to maintain memory.")

        # Construct the response data
        session_summary = {
            "total_flashcards": total_flashcards,
            "remembered": remembered,
            "forgotten": forgotten,
            "suggestions": suggestions
        }


        return Response({"session_summary": session_summary})

