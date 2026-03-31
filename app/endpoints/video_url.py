import re
from flask import Blueprint, request, jsonify
from app.authorization import login_decorator
from app.logic.fetch_video import fetch_info

router = Blueprint('video_url', __name__)

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


@router.route("/video-url", methods=["GET"])
@login_decorator
def video_url():
    videoId = request.args.get("videoId")
    
    if not videoId or not VIDEO_ID_RE.fullmatch(videoId):
        return jsonify(
            {"error": "Nieprawidłowy videoId: oczekiwane 11 znaków [A-Za-z0-9_-]"}
        ), 400

    try:
        info = fetch_info(videoId)
    except Exception as e:
        return jsonify(
            {"error": "Błąd przetwarzania", "details": str(e)}
        ), 500

    chosen = next(
        (
            f
            for f in info.get("formats", [])
            if f.get("vcodec") != "none" and f.get("acodec") != "none"
        ),
        None,
    )

    if not chosen or "url" not in chosen:
        return jsonify({"error": "Brak formatu audio+video"}), 500

    return jsonify({
        "title": info.get("title"),
        "format": chosen.get("format_id"),
        "ext": chosen.get("ext"),
        "mime_type": chosen.get("mime_type"),
        "url": chosen.get("url"),
        "expires_in": info.get("_signature_timestamp"),
    })
