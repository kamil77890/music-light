from flask import Blueprint, request, send_file, abort
import os
from app.logic.ultimate_downloader import download_song, download_playlist
from app.authorization import login_decorator

router = Blueprint('download', __name__)


@router.route("/download", methods=["GET"])
@login_decorator
def download():
    videoId = request.args.get("videoId", "0")
    song_id = request.args.get("id", "0")
    playlistId = request.args.get("playlistId", "0")
    format = request.args.get("format", "mp3")

    if playlistId != "0":
        file_path = download_playlist(playlistId, song_id, format)
    else:
        file_path = download_song(videoId, song_id, format)

    if not os.path.exists(file_path):
        abort(404, description="File not found")
    
    return send_file(
        file_path,
        as_attachment=True,
        download_name=os.path.basename(file_path),
        mimetype="application/octet-stream"
    )
