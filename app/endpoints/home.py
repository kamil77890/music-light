from flask import Blueprint, jsonify

router = Blueprint('home', __name__)


@router.route("/", methods=["GET"])
def home():
    return jsonify({
        "/cloud/config": "GET /cloud/config",
        "/cloud/catalog": "GET /cloud/catalog?max_keys=50",
        "/cloud/upload": 'POST /cloud/upload (Body: {"directory": "/optional/path"})',
        "/download": "GET /download?videoId=dQw4w9WgXcQ&format=mp3",
        "/songs/{filename}": "GET /songs/NeverGonnaGiveYouUp.mp3",
        "/search": "GET /search?q=Linkin+Park&return_playlists=true",
        "/subtitles": "GET /subtitles?videoId=dQw4w9WgXcQ&lang=en",
        "/api/songs": "GET /api/songs",
        "/get/id": "GET /get/id",
        "/title": "GET /title?videoId=dQw4w9WgXcQ",
        "/Register": "GET /Register (Headers: {'token': 'your_token'})"
    })
