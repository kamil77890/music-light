import os
from yt_dlp import YoutubeDL


def download_song_mp3(url: str, base_path: str, audio_format: str = "mp3", quality: str = "320", download_subs: bool = False) -> dict:
    """Download a YouTube video as audio"""
    os.makedirs(base_path, exist_ok=True)

    cookie_path = os.path.abspath("../cookies.txt")

    base_opts = {
        "quiet": True,
        "no_warnings": True,
        "proxy": "",
        "nocheckcertificate": True,
        "geo_bypass": True,
        "http_headers": {"User-Agent": "Mozilla/5.0"},
    }

    if os.path.exists(cookie_path):
        base_opts["cookiefile"] = cookie_path

    temp_opts = {**base_opts, "skip_download": True}
    with YoutubeDL(temp_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    entries = info.get("entries") or [info]
    downloaded_files = []

    for entry in entries:
        title = entry.get("title", "audio")
        safe_title = "".join(c for c in title if c.isalnum() or c in " _-").rstrip()
        outtmpl = os.path.join(base_path, safe_title + ".%(ext)s")

        opts = {
            **base_opts,
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
                "preferredquality": quality,
            }],
            "writesubtitles": download_subs,
            "writeautomaticsub": download_subs,
            "subtitlesformat": "vtt",
            "subtitleslangs": ["en"],
            "quiet": False,
            "ignoreerrors": True,
        }

        with YoutubeDL(opts) as ydl:
            ydl.download([entry.get("webpage_url")])

        downloaded_files.append(os.path.join(base_path, safe_title + f".{audio_format}"))

    return {"info": info, "downloaded_files": downloaded_files}
