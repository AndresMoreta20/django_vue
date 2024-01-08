from django.shortcuts import render
from .models import UserSavedLecturespace, UserSavedFlashcard, Lecturespace
from .forms import LecturespaceForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from googleapiclient.discovery import build
from django.conf import settings; 
import re
import openai 
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm

def index(request):
    return render(request, 'index.html')

def user_dashboard(request):
    saved_lecturespaces = UserSavedLecturespace.objects.filter(user=request.user)
    saved_flashcards = UserSavedFlashcard.objects.filter(user=request.user)
    return render(request, 'lecturespaces/user_dashboard.html', {
        'saved_lecturespaces': saved_lecturespaces,
        'saved_flashcards': saved_flashcards
    })


def create_lecturespace(request):
    if request.method == 'POST':
        form = LecturespaceForm(request.POST)
        if form.is_valid():
            lecturespace = form.save(commit=False)
            lecturespace.created_by = request.user
            lecturespace.save()
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

def extract_video_id(youtube_url):
    # Regex patterns for different YouTube URL formats
    regex_patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)'
    ]

    for pattern in regex_patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)

    return None  # Return None if no video ID is found

def fetch_youtube_video_details(youtube_url):
    video_id = extract_video_id(youtube_url)
    if not video_id:
        return None  # Handle cases where the video ID couldn't be extracted

    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()

    # Extract relevant data from response
    if 'items' in response and len(response['items']) > 0:
        item = response['items'][0]
        title = item['snippet']['title']
        tags = item.get('snippet', {}).get('tags', [])
        return {'title': title, 'tags': tags}

    return None  # Return None if no data is fetched

def extract_random_sequence(script, sequence_length=10):
    """
    Extract a random sequence of words from the video script.

    :param script: The full text of the video script.
    :param sequence_length: The number of consecutive words in the sequence.
    :return: A string containing the extracted sequence of words.
    """
    words = script.split()
    if len(words) < sequence_length:
        return None  # Return None if the script is too short

    start_index = random.randint(0, len(words) - sequence_length)
    return ' '.join(words[start_index:start_index + sequence_length])


def make_openai_request(prompt, max_tokens):
    openai.api_key = settings.GPT_API_KEY

    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def create_flashcard_from_sequence(sequence):
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
    return None, None

def create_flashcard_from_title(title):
    prompt = f"Create a detailed and informative flashcard based on the following video title: {title}"
    content = make_openai_request(prompt, 150)
    return title, content

def create_flashcard_based_on_availability(script, video_title):
    if script:
        sequence = extract_random_sequence(script)
        return create_flashcard_from_sequence(sequence)
    else:
        return create_flashcard_from_title(video_title)
    
@login_required
def home(request):
    return render(request, 'lecturespaces/home.html')

@login_required
def create_lecturespace(request):
    """
    View for creating a new Lecturespace. Handles form submission and
    fetches video details using the YouTube API.

    :param request: The HTTP request object.
    :return: The rendered response.
    """
    if request.method == 'POST':
        form = LecturespaceForm(request.POST)
        if form.is_valid():
            lecturespace = form.save(commit=False)
            lecturespace.created_by = request.user

            # Fetch YouTube video details
            youtube_url = form.cleaned_data.get('youtube_url')
            video_details = fetch_youtube_video_details(youtube_url)
            if video_details:
                lecturespace.title = video_details.get('title')
                # Add tags or other details if needed

            lecturespace.save()

            # Optional: Initiate flashcard generation process
            # This can be done here or in a background task depending on your app's architecture

            return redirect('lecturespace_detail', lecturespace_id=lecturespace.id)
    else:
        form = LecturespaceForm()

    return render(request, 'lecturespaces/create_lecturespace.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            print("Invalid credentials")
    return render(request, 'lecturespaces/login.html')

def logout(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})