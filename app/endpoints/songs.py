from flask import Blueprint, jsonify
from app.authorization import login_decorator
from ..db.db_controller import DbController

router = Blueprint('songs', __name__, url_prefix='/api')
db = DbController()


@router.route("/songs", methods=["GET"])
@login_decorator
def get_songs():
    try:
        data = db.get_all_songs()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
