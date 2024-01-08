from django import template
import re

register = template.Library()

@register.simple_tag
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
