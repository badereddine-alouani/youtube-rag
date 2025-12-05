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
