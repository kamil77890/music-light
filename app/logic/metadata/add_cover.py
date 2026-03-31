"""
add_cover.py - Module for embedding cover art into audio files
"""

import os
from typing import Optional

import requests
from mutagen.id3 import ID3, ID3NoHeaderError, APIC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover


def _detect_mime(image_bytes: bytes) -> str:
    if image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if image_bytes.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    return "image/jpeg"


def _fetch_image(image_url: str) -> Optional[bytes]:
    try:
        resp = requests.get(image_url, timeout=15)
        resp.raise_for_status()
        return resp.content
    except Exception:
        return None


def embed_image_mp3(
    file_path: str,
    image_url: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    mime: Optional[str] = None,
) -> bool:
    if not os.path.exists(file_path):
        return False

    if image_url is not None:
        image_bytes = _fetch_image(image_url)

    if not image_bytes:
        return False

    mime = mime or _detect_mime(image_bytes)

    try:
        try:
            tags = ID3(file_path)
        except ID3NoHeaderError:
            try:
                audio = MP3(file_path)
                audio.add_tags()
                audio.save()
                tags = ID3(file_path)
            except Exception:
                return False

        tags.delall("APIC")
        tags.add(APIC(encoding=3, mime=mime, type=3, desc="Cover", data=image_bytes))
        tags.save(file_path, v2_version=3)
        return True

    except Exception:
        return False


def embed_image_mp4(
    file_path: str,
    image_url: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> bool:
    if not os.path.exists(file_path):
        return False

    if image_url is not None:
        image_bytes = _fetch_image(image_url)

    if not image_bytes:
        return False

    try:
        imageformat = MP4Cover.FORMAT_PNG if _detect_mime(image_bytes) == "image/png" else MP4Cover.FORMAT_JPEG
        mp4 = MP4(file_path)
        mp4["covr"] = [MP4Cover(image_bytes, imageformat=imageformat)]
        mp4.save()
        return True

    except Exception:
        return False