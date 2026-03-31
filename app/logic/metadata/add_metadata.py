import os
import asyncio
from typing import Optional
from mutagen.id3 import ID3, TIT2, TPE1, TCON, ID3NoHeaderError
from mutagen.mp4 import MP4

from app.logic.api_handler.handle_yt import get_song_by_string
from app.logic.metadata.add_cover import embed_image_mp3, embed_image_mp4


def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            return new_loop.run_until_complete(coro)
        finally:
            new_loop.close()
            asyncio.set_event_loop(loop)

    return loop.run_until_complete(coro)


def _extract_song_fields(song_data) -> dict:
    """Normalize varying response shapes into a flat dict with title, artist, thumbnail_url."""
    result = {"title": None, "artist": None, "thumbnail_url": None}

    song = song_data[0] if isinstance(song_data, list) else song_data
    if not song:
        return result

    if isinstance(song, dict):
        snippet = song.get("snippet", {})
        result["title"] = snippet.get("title")
        result["artist"] = snippet.get("channelTitle")
        thumbnails = snippet.get("thumbnails", {})
    elif hasattr(song, "snippet"):
        snippet = song.snippet
        result["title"] = getattr(snippet, "title", None)
        result["artist"] = getattr(snippet, "channelTitle", None) or getattr(snippet, "channel_title", None)
        thumbnails = getattr(snippet, "thumbnails", None)
    else:
        return result

    result["thumbnail_url"] = _extract_thumbnail_url(thumbnails)
    return result


def _extract_thumbnail_url(thumbnails) -> Optional[str]:
    if not thumbnails:
        return None

    priority = ("maxres", "standard", "high", "medium", "default")

    if isinstance(thumbnails, dict):
        for key in priority:
            url = thumbnails.get(key, {}).get("url")
            if url:
                return url
        return None

    for key in priority:
        thumb = getattr(thumbnails, key, None)
        if not thumb:
            continue
        if hasattr(thumb, "url"):
            return thumb.url
        if isinstance(thumb, dict):
            return thumb.get("url")

    return None


def add_metadata(file_path: str, format: str, video_id: str) -> bool:
    if not os.path.exists(file_path) or not video_id or len(video_id) != 11:
        return False

    try:
        song_data = _run_async(get_song_by_string(video_id))
        if not song_data:
            return False
        fields = _extract_song_fields(song_data)
    except Exception:
        return False

    title = fields["title"] or "Unknown Title"
    artist = fields["artist"] or "Unknown Artist"
    thumbnail_url = fields["thumbnail_url"]

    fmt = format.lower()

    if fmt == "mp3":
        return _write_mp3_metadata(file_path, title, artist, video_id, thumbnail_url)

    if fmt in ("mp4", "m4a"):
        return _write_mp4_metadata(file_path, title, artist, video_id, thumbnail_url)

    return False


def _write_mp3_metadata(
    file_path: str, title: str, artist: str, video_id: str, thumbnail_url: Optional[str]
) -> bool:
    try:
        try:
            id3 = ID3(file_path)
        except ID3NoHeaderError:
            id3 = ID3()

        id3.add(TIT2(encoding=3, text=title))
        id3.add(TPE1(encoding=3, text=artist))
        id3.add(TCON(encoding=3, text=video_id))
        id3.save(file_path, v2_version=3)

        if thumbnail_url:
            embed_image_mp3(file_path, image_url=thumbnail_url)

        return True
    except Exception:
        return False


def _write_mp4_metadata(
    file_path: str, title: str, artist: str, video_id: str, thumbnail_url: Optional[str]
) -> bool:
    try:
        audio = MP4(file_path)
        audio["\xa9nam"] = title
        audio["\xa9ART"] = artist
        audio["\xa9cmt"] = video_id
        audio.save()

        if thumbnail_url:
            embed_image_mp4(file_path, image_url=thumbnail_url)

        return True
    except Exception:
        return False


def verify_metadata(file_path: str, format: str) -> dict:
    try:
        if format.lower() == "mp3":
            id3 = ID3(file_path)
            return {
                "title": str(id3.get("TIT2", "N/A")),
                "artist": str(id3.get("TPE1", "N/A")),
                "video_id": str(id3.get("TCON", "N/A")),
                "has_cover": any(k.startswith("APIC") for k in id3.keys()),
            }

        if format.lower() in ("mp4", "m4a"):
            audio = MP4(file_path)
            return {
                "title": audio.get("\xa9nam", ["N/A"])[0],
                "artist": audio.get("\xa9ART", ["N/A"])[0],
                "video_id": audio.get("\xa9cmt", ["N/A"])[0],
                "has_cover": "covr" in audio,
            }
    except Exception:
        pass

    return {}