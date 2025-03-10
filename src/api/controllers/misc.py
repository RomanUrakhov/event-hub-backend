import os
from flask import Blueprint, current_app, jsonify, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from uuid import uuid4

# TODO: refactor this mess

ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def create_misc_blueprint():
    bp = Blueprint("misc", __name__)

    @bp.route("/images/<string:image_id>", methods=["GET"])
    def get_image(image_id: str):
        response = send_from_directory(
            f'{current_app.config["APPLICATION_STATIC_DIR"]}/images', image_id
        )
        return response

    @bp.route("/images", methods=["POST"])
    def upload_image():
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]

        if not file or not file.filename:
            return jsonify({"error": "No selected file"}), 400

        if allowed_file(file.filename):
            file_id = str(uuid4())
            filename = secure_filename(file.filename)
            filename = f"{file_id}{filename}"
            file.save(
                os.path.join(
                    current_app.config["APPLICATION_STATIC_DIR"], "images", filename
                )
            )
            return jsonify(
                {
                    "id": filename,
                    "url": url_for("misc.get_image", image_id=filename, _external=True),
                }
            ), 201
        else:
            return jsonify({"error": "Not allowed file format"}), 400

    return bp
