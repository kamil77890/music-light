from __future__ import annotations

import logging
import os
import traceback
from typing import Optional

from flask import Blueprint, request, jsonify

from app.config.stałe import Parameters
from app.logic import b2_storage

logger = logging.getLogger("werkzeug")

router = Blueprint('cloud', __name__, url_prefix='/cloud')


@router.route("/config", methods=["GET"])
def cloud_config():
    try:
        return jsonify(b2_storage.get_cloud_config())
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


def _b2_catalog_detail(exc: Exception) -> str:
    s = str(exc)
    if "SignatureDoesNotMatch" in s:
        return (
            f"{s} — Check .env: B2_KEY_ID + B2_APPLICATION_KEY must be the same key pair from "
            "Backblaze (Application Keys), ENDPOINT_URL = S3 endpoint for that bucket, no spaces/quotes."
        )
    return s


@router.route("/catalog", methods=["GET"])
def cloud_catalog():
    """List audio objects under `music/` with direct HTTPS URLs."""
    max_keys = request.args.get("max_keys", 500, type=int)
    try:
        items = b2_storage.list_music_objects(max_keys=max_keys)
        return jsonify({"items": items, "count": len(items)})
    except Exception as exc:
        logger.exception("GET /cloud/catalog failed: %s", exc)
        traceback.print_exc()
        return jsonify({"error": _b2_catalog_detail(exc)}), 500


@router.route("/upload", methods=["POST"])
def cloud_upload():
    """
    Upload all local audio files from the download directory to B2 under `music/`.
    Uses the same root as the app (`FILEPATH` env or default).
    """
    data = request.get_json(silent=True) or {}
    root = data.get("directory") or Parameters.get_download_dir()
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        return jsonify({"error": f"Directory not found: {root}"}), 400

    try:
        up, fail = b2_storage.upload_directory_to_b2(root, prefix="music")
        return jsonify({"ok": True, "uploaded": up, "failed": fail, "root": root})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
