from flask import Blueprint, request, send_file, jsonify
from app.authorization import login_decorator
from app.logic.subtitles.subtitles_downloader import get_subtitles_as_txt

router = Blueprint('subtitles', __name__)


@router.route("/subtitles", methods=["GET"])
@login_decorator
def get_subtitles_txt():
    videoId = request.args.get("videoId")
    lang = request.args.get("lang", "en")
    
    if not videoId:
        return jsonify({"error": "Missing videoId"}), 400

    try:
        txt_path = get_subtitles_as_txt(videoId, lang)
        return send_file(
            txt_path,
            as_attachment=True,
            download_name=f"{videoId}.txt",
            mimetype="text/plain"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
