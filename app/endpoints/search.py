from flask import Blueprint, request, jsonify
import json
from app.exceptions.youtube_errors import (
    YouTubeQuotaExceededError,
    YouTubeAccessDeniedError,
    YouTubeAPIError,
)
from app.logic.api_handler.handle_yt import get_song_by_string
from app.logic.api_handler.handle_playlist_search import (
    get_playlist_search,
    get_playlist_songs_paginated,
)

router = Blueprint('search', __name__)


@router.route("/search", methods=["GET"])
def search_songs():
    q = request.args.get("q", "")
    pageToken = request.args.get("pageToken", None)
    return_playlists = request.args.get("return_playlists", "false").lower() == "true"
    playlistPageTokens_str = request.args.get("playlistPageTokens", "{}")

    try:
        playlist_tokens_dict = json.loads(playlistPageTokens_str)
    except:
        playlist_tokens_dict = {}

    try:
        results = get_song_by_string(user_input=q, page_token=pageToken)

        playlists_data = []
        if return_playlists:
            playlists = get_playlist_search(q)
            for pl in playlists:
                playlist_id = pl["id"]["playlistId"]
                token_for_this_playlist = playlist_tokens_dict.get(playlist_id)

                songs_data = get_playlist_songs_paginated(
                    playlist_id,
                    page_token=token_for_this_playlist,
                    page_size=10
                )

                playlists_data.append({
                    "playlist": pl,
                    "songs": songs_data["songs"],
                    "nextPageToken": songs_data.get("nextPageToken")
                })

        return jsonify({
            "success": True,
            "data": results,
            "playlists": playlists_data
        })

    except YouTubeQuotaExceededError as e:
        return jsonify({
            "error": "QUOTA_EXCEEDED",
            "message": str(e),
            "solution": "Please try again tomorrow or contact administrator"
        }), 429
    except YouTubeAccessDeniedError as e:
        return jsonify({
            "error": "ACCESS_DENIED",
            "message": str(e),
            "solution": "Check your YouTube API key configuration"
        }), 403
    except YouTubeAPIError as e:
        return jsonify({
            "error": "YOUTUBE_API_ERROR",
            "message": str(e),
            "solution": "Please try again later"
        }), 500
