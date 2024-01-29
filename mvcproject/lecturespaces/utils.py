# utils.py

import random
import re
import os
from datetime import datetime
from googleapiclient.discovery import build
from .models import Tag, Flashcard
import openai
# Import any necessary libraries for YouTube API interaction, e.g., googleapiclient
from googleapiclient.discovery import build
# You might also need standard Python libraries, depending on your implementation
import requests



def extract_video_id(youtube_url):
    regex_patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)'
    ]

    for pattern in regex_patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    return None

def fetch_youtube_video_details(youtube_url):
    video_id = extract_video_id(youtube_url)
    if not video_id:
        return None

    youtube = build('youtube', 'v3', developerKey=os.environ.get('YOUTUBE_API_KEY'))
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()

    if 'items' in response and len(response['items']) > 0:
        item = response['items'][0]
        title = item['snippet']['title']
        tags = item.get('snippet', {}).get('tags', [])
        return {'title': title, 'tags': tags}
    return None

def extract_random_sequence(script, sequence_length=10):
    words = script.split()
    if len(words) < sequence_length:
        return None

    start_index = random.randint(0, len(words) - sequence_length)
    return ' '.join(words[start_index:start_index + sequence_length])

def make_openai_request(prompt, max_tokens):
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
        return None

def create_flashcard_from_sequence(sequence):
    prompt = f"Create a concise flashcard with a title (up to 5 words) and content (up to 10 words) based on the following information:\n\n{sequence}"
    response_text = make_openai_request(prompt, 60)
    return _process_openai_flashcard_response(response_text)

def create_flashcard_from_title(title):
    prompt = f"Create a flashcard with a concise title (up to 5 words max) and detailed content (up to 10 words max) based on the following youtube video: {title}"
    response_text = make_openai_request(prompt, 100)
    return _process_openai_flashcard_response(response_text)

def _process_openai_flashcard_response(response_text):
    if response_text:
        parts = response_text.split("\n")
        if len(parts) >= 2:
            title = parts[0].replace("Title:", "").strip().split()[:5]
            content = parts[1].replace("Content:", "").strip().split()[:10]
            return ' '.join(title), ' '.join(content)
    return None, None

def check_and_delete_flashcard_if_needed(flashcard):
    total_votes = flashcard.likes + flashcard.dislikes
    if total_votes > 5:
        dislike_ratio = flashcard.dislikes / total_votes
        if dislike_ratio >= 0.4:
            flashcard.delete()
            return True
    return False


def fetch_youtube_video_details_and_create_tags(youtube_url):
    video_details = fetch_youtube_video_details(youtube_url)
    tags = []
    if video_details:
        for tag_name in video_details.get('tags', []):
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
    return video_details, tags
