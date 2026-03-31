from flask import Blueprint, request, jsonify
from app.authorization import login_decorator
from app.logic.api_handler.handle_yt import get_song_by_string

router = Blueprint('song_title', __name__)


@router.route("/title", methods=["GET"])
@login_decorator
def get_title():
    videoId = request.args.get("videoId")
    if not videoId:
        return jsonify({"error": "Missing videoId"}), 400
    
    song_data = get_song_by_string(videoId)
    snippet = song_data[0]["snippet"]
    title = snippet["title"]
    return jsonify({"title": title})
