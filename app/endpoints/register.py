from flask import Blueprint, request, jsonify
from app.authorization import login_decorator

router = Blueprint('register', __name__)

TOKEN = {"token": ""}


@router.route("/Register", methods=["GET"])
@login_decorator
def register():
    token = request.headers.get("token")
    TOKEN["token"] = token
    return jsonify({"TOKEN": TOKEN["token"]})
