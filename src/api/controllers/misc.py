from flask import Blueprint, current_app, send_from_directory


def create_misc_blueprint():
    bp = Blueprint("misc", __name__)

    @bp.route("/images/<string:image_id>", methods=["GET"])
    def get_image(image_id: str):
        response = send_from_directory(
            current_app.config["APPLICATION_STATIC_DIR"], "gendalf.jpg"
        )
        return response

    return bp
