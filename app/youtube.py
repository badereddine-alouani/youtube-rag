from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


def extract_video_id(url):
    parsed = urlparse(url)

    if parsed.hostname in ["youtu.be"]:
        return parsed.path.lstrip("/")

    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        elif parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[2]
        elif parsed.path.startswith("/v/"):
            return parsed.path.split("/")[2]
        elif parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]

    raise ValueError("Invalid YouTube URL format")


def get_transcript(url):
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL: could not extract video ID")

    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=["en", "ar", "fr"]
        )
        return " ".join([t["text"] for t in transcript])
    except Exception as e:
        raise RuntimeError(f"Failed to get transcript: {str(e)}")
