from flask import Blueprint, request, send_file, abort
import os
from ..config.stałe import Parameters
from app.authorization import login_decorator

router = Blueprint('file_download', __name__)


@router.route("/songs/<path:filename>", methods=["GET"])
@login_decorator
def download_file(filename):
    file_path = os.path.join(Parameters.get_download_dir(), filename)
    if not os.path.isfile(file_path):
        abort(404, description="File not found")
    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/octet-stream"
    )
