import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def extract_video_id(url: str) -> str:
    """Extracts the video ID from a YouTube URL."""
    # Handle various YouTube URL formats
    patterns = [
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)",
        r"(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)",
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
            
    raise ValueError("Invalid YouTube URL")

def get_video_transcript(video_id: str) -> list[dict]:
    """Fetches the transcript for a given YouTube video ID."""
    try:
        # Get the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        raise Exception(f"Failed to fetch transcript: {str(e)}")

def get_transcript_text(transcript: list[dict]) -> str:
    """Converts the transcript dictionary list to a single text string."""
    formatter = TextFormatter()
    return formatter.format_transcript(transcript)
