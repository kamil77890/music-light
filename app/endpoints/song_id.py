from flask import Blueprint, jsonify
from app.authorization import login_decorator
from ..db.db_controller import DbController

router = Blueprint('song_id', __name__)

db = DbController()


@router.route("/get/id", methods=["GET"])
@login_decorator
def get_songs():
    try:
        last_id = db.get_last_song_id()
        return jsonify(last_id if last_id is not None else 0)
    except Exception as e:
        return jsonify({"error": str(e)})
