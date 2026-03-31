from flask import request, jsonify
from functools import wraps


def login_decorator(endpoint):
    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        token = request.headers.get("token")
        if token == "cos":
            return endpoint(*args, **kwargs)
        else:
            return jsonify({"error": "Brak dostępu"}), 403
    return wrapper
