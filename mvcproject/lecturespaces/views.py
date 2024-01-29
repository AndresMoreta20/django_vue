# Standard library imports
from datetime import datetime
import os
import re
import random

# Django imports
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.db.models import Count
from django.conf import settings

# Google and third-party imports
from googleapiclient.discovery import build
from google.cloud import kms
import openai

# Local app imports
from .models import Flashcard, FlashcardVote, Tag, UserSavedLecturespace, UserSavedFlashcard, Lecturespace
from .forms import LecturespaceForm, UserRegisterForm
from django.contrib.auth.forms import UserCreationForm
from collections import Counter

from .services.user_dashboard_service import get_user_saved_data, process_tags

from .flashcard_strategies.sequence_based_strategy import SequenceBasedFlashcardStrategy
from .flashcard_strategies.title_based_strategy import TitleBasedFlashcardStrategy



from .utils import (
    extract_video_id, fetch_youtube_video_details, create_flashcard_from_sequence,
    create_flashcard_from_title, check_and_delete_flashcard_if_needed, fetch_youtube_video_details_and_create_tags
)



def index(request):
    return render(request, 'index.html')


@login_required
def user_dashboard(request):
    saved_lecturespaces, saved_flashcards = get_user_saved_data(request.user)
    most_common_tags = process_tags(saved_lecturespaces)

    recommended_lecturespaces = []
    if most_common_tags:
        most_common_tag = most_common_tags[0][0]
        recommended_lecturespaces = Lecturespace.objects.filter(
            tags__name=most_common_tag
        ).exclude(
            id__in=[saved_ls.lecturespace.id for saved_ls in saved_lecturespaces]
        ).distinct()[:10]

    return render(request, 'lecturespaces/user_dashboard.html', {
        'saved_lecturespaces': saved_lecturespaces,
        'saved_flashcards': saved_flashcards,
        'recommended_lecturespaces': recommended_lecturespaces
    })

# @login_required
def check_session(request):
    return JsonResponse({'session_active': request.user.is_authenticated})


def date_tags(request):
    tags = None

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            tags = Lecturespace.objects.filter(
                created_at__range=[start_date, end_date]
            ).values_list('tags__name').annotate(
                num_times=Count('tags')
            ).order_by('-num_times')

    return render(request, 'lecturespaces/date_tags.html', {'tags': tags})







@login_required
def create_lecturespace(request):
    if request.method == 'POST':
        form = LecturespaceForm(request.POST)
        if form.is_valid():
            lecturespace = form.save(commit=False)
            lecturespace.created_by = request.user

            youtube_url = form.cleaned_data.get('youtube_url')
            video_details, tags = fetch_youtube_video_details_and_create_tags(youtube_url)

            if video_details:
                lecturespace.title = video_details.get('title')
                lecturespace.save()
                lecturespace.tags.set(tags)

            return redirect('lecturespace_detail', lecturespace_id=lecturespace.id)
    else:
        form = LecturespaceForm()

    return render(request, 'lecturespaces/create_lecturespace.html', {'form': form})



def explore_lecturespaces(request):
    lecturespaces = Lecturespace.objects.all()
    return render(request, 'lecturespaces/explore_lecturespaces.html', {'lecturespaces': lecturespaces})

def lecturespace_detail(request, lecturespace_id):
    lecturespace = get_object_or_404(Lecturespace, id=lecturespace_id)
    return render(request, 'lecturespaces/lecturespace_detail.html', {'lecturespace': lecturespace})
def extract_random_sequence(script, sequence_length=10):

    words = script.split()
    if len(words) < sequence_length:
        return None  # Return None if the script is too short

    start_index = random.randint(0, len(words) - sequence_length)
    return ' '.join(words[start_index:start_index + sequence_length])




def create_flashcard_based_on_availability(script, video_title):
    if script:
        strategy = SequenceBasedFlashcardStrategy()
    else:
        strategy = TitleBasedFlashcardStrategy()

    return strategy.create_flashcard(script if script else video_title)






    
@login_required
def home(request):
    return render(request, 'lecturespaces/home.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('admin')  # Redirect to admin dashboard
            else:
                return redirect('user_dashboard')  # Redirect to user dashboard or another page
        else:
            messages.error(request, 'Invalid username or password.')

    return redirect('home')

def logout(request):
    auth_logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def create_flashcard(request, lecturespace_id):
    lecturespace = get_object_or_404(Lecturespace, id=lecturespace_id)

    if request.method == 'POST':
        flashcard_title, flashcard_content = create_flashcard_from_title(lecturespace.title)
        if flashcard_title and flashcard_content:
            flashcard = Flashcard.objects.create(
                lecturespace=lecturespace,
                title=flashcard_title,
                content=flashcard_content
            )
            print(f"Flashcard created successfully.")
            print("Title:", flashcard.title)
            print("Content:", flashcard.content)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required
def create_and_save_flashcard(request, lecturespace_id):
    if request.method == 'POST':
         # Replace with your actual OpenAI API key
        client = openai.OpenAI(api_key='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' )
        try:
            lecturespace = get_object_or_404(Lecturespace, id=lecturespace_id)
            prompt = f"Create a flashcard with a concise title (up to 5 words max) and detailed content (up to 10 words max) from any random topic covered in this youtube video:  {lecturespace.title}. The title could be a Question or some text that reference a concept. The content is the explanation of this concept or answer to the question. Be direct and focus on the content, do not add informative text. The format must be this: Title: [title] Content: [content]"
            #prompt = f"Create a flashcard with a concise title and detailed content based on the following YouTube video: {lecturespace.title}."
            chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            max_tokens=100,
            temperature=1
            )
            response_text = chat_completion.choices[0].message.content.strip()

            if response_text:
                # Split the response by lines
                lines = response_text.split("\n")

                # Initialize variables for the flashcard title and content
                flashcard_title = ""
                flashcard_content = ""

                # Loop through the lines to find and extract Title and Content
                for line in lines:
                    if line.startswith("Title:"):
                        flashcard_title = line.replace("Title:", "").strip()
                    elif line.startswith("Content:"):
                        flashcard_content = line.replace("Content:", "").strip()

                # Check if both title and content were found
                if flashcard_title and flashcard_content:
                    # Create the flashcard
                    Flashcard.objects.create(
                        lecturespace=lecturespace,
                        title=flashcard_title,
                        content=flashcard_content
                    )
                    print("Flashcard created successfully.")
                else:
                    print("Error: Title and Content not found in the response text.")
            else:
                print("Error: Response text is empty.")

        except Exception as e:
            print(f"An error occurred: {e}")
    messages.info(request, 'Creating flashcard...')
    # Redirect back to the referring page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required
def save_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    UserSavedFlashcard.objects.get_or_create(user=request.user, flashcard=flashcard)
    return redirect('lecturespace_detail', lecturespace_id=flashcard.lecturespace.id)

@login_required
def like_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    vote, created = FlashcardVote.objects.get_or_create(user=request.user, flashcard=flashcard, defaults={'like': True})
    deleted = check_and_delete_flashcard_if_needed(flashcard)
    if deleted:
        messages.info(request, "The flashcard has been deleted due to high dislikes.")
        return redirect('lecturespace_detail', lecturespace_id=flashcard.lecturespace.id)
    if created:
        flashcard.likes += 1
        flashcard.save()
    elif not vote.like:  # If changing from dislike to like
        flashcard.likes += 1
        flashcard.dislikes -= 1
        flashcard.save()
        vote.like = True
        vote.save()

    return redirect('lecturespace_detail', lecturespace_id=flashcard.lecturespace.id)


@login_required
def dislike_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    vote, created = FlashcardVote.objects.get_or_create(user=request.user, flashcard=flashcard, defaults={'like': False})
    deleted = check_and_delete_flashcard_if_needed(flashcard)
    if deleted:
        messages.info(request, "The flashcard has been deleted due to high dislikes.")
        return redirect('lecturespace_detail', lecturespace_id=flashcard.lecturespace.id)
    if created:
        flashcard.dislikes += 1
        flashcard.save()
    elif vote.like:  # If changing from like to dislike
        flashcard.dislikes += 1
        flashcard.likes -= 1
        flashcard.save()
        vote.like = False
        vote.save()

    return redirect('lecturespace_detail', lecturespace_id=flashcard.lecturespace.id)

@login_required
def save_lecturespace(request, lecturespace_id):
    lecturespace = get_object_or_404(Lecturespace, id=lecturespace_id)
    UserSavedLecturespace.objects.get_or_create(user=request.user, lecturespace=lecturespace)
    return redirect('lecturespace_detail', lecturespace_id=lecturespace.id)

@login_required
def unsave_lecturespace(request, lecturespace_id):
    lecturespace = get_object_or_404(Lecturespace, id=lecturespace_id)

    try:
        saved_lecturespace = UserSavedLecturespace.objects.get(user=request.user, lecturespace=lecturespace)
        saved_lecturespace.delete()
        messages.success(request, "Lecturespace removed from your saved list.")
    except UserSavedLecturespace.DoesNotExist:
        messages.error(request, "This lecturespace is not in your saved list.")

    return redirect('user_dashboard')

@login_required
def unsave_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id)

    try:
        saved_flashcard = UserSavedFlashcard.objects.get(user=request.user, flashcard=flashcard)
        saved_flashcard.delete()
        messages.success(request, "Flashcard removed from your saved list.")
    except UserSavedFlashcard.DoesNotExist:
        messages.error(request, "This flashcard is not in your saved list.")

    return redirect('user_dashboard')


def extract_id(youtube_url):
    regex_patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)'
    ]

    for pattern in regex_patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)

    return None




'''def extract_video_id(youtube_url):
    # Regex patterns for different YouTube URL formats
    regex_patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)'
    ]

    for pattern in regex_patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)

    return None  # Return None if no video ID is found'''

'''def fetch_youtube_video_details(youtube_url):
    video_id = extract_video_id(youtube_url)
    if not video_id:
        return None  # Handle cases where the video ID couldn't be extracted

    youtube = build('youtube', 'v3', developerKey=os.environ.get('YOUTUBE_API_KEY'))
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()

    # Extract relevant data from response
    if 'items' in response and len(response['items']) > 0:
        item = response['items'][0]
        title = item['snippet']['title']
        tags = item.get('snippet', {}).get('tags', [])
        return {'title': title, 'tags': tags}

    return None  # Return None if no data is fetched'''

'''
def check_and_delete_flashcard_if_needed(flashcard):
    total_votes = flashcard.likes + flashcard.dislikes
    if total_votes > 5:
        dislike_ratio = flashcard.dislikes / total_votes
        if dislike_ratio >= 0.4:  # 40% or more dislikes
            flashcard.delete()
            return True  # Indicates the flashcard was deleted
    return False  # Indicates the flashcard was not deleted
'''

'''def make_openai_request(prompt, max_tokens):
   client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

   try:
       chat_completion = client.chat.completions.create(
           messages=[
               {"role": "system", "content": "You are a helpful assistant."},
               {"role": "user", "content": prompt}
           ],
           model="gpt-3.5-turbo",
           max_tokens=max_tokens
       )
       return chat_completion.choices[0].message.content.strip()
   except Exception as e:
       print(f"An error occurred: {e}")
       return None'''

'''def create_flashcard_from_sequence(sequence):
    prompt = f"Create a concise flashcard with a title (up to 5 words) and content (up to 10 words) based on the following information:\n\n{sequence}"
    response_text = make_openai_request(prompt, 60)
    if response_text:
        # Split the response text to separate the title and content
        # Assuming the format "Title: [title]\nContent: [content]"
        parts = response_text.split("\n")
        if len(parts) >= 2:
            title = parts[0].replace("Title:", "").strip().split()[:5]
            content = parts[1].replace("Content:", "").strip().split()[:10]
            return ' '.join(title), ' '.join(content)
        else:
            print("Unexpected response format from OpenAI API.")
    return None, None'''


'''def create_flashcard_from_title(title):
    prompt = f"Create a flashcard with a concise title (up to 5 words max) and detailed content (up to 10 words max) based on the following youtube video: {title}. The title could be a Question or some text that reference a concept. The content is the explanation of this concept or answer to the question. Be direct and focus on the content, do not add informative text"
    response_text = make_openai_request(prompt, 100)
    if response_text:
        # Split the response text to separate the title and content
        parts = response_text.split("\n")
        if len(parts) >= 2:
            flashcard_title = parts[0].replace("Title:", "").strip().split()[:5]
            flashcard_content = parts[1].replace("Content:", "").strip().split()[:50]
            return ' '.join(flashcard_title), ' '.join(flashcard_content)
        else:
            print("Unexpected response format from OpenAI API.")
    return None, None'''