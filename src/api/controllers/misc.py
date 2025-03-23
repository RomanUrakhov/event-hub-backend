import os
from flask import current_app, send_from_directory
from apiflask import APIBlueprint, FileSchema, abort
from werkzeug.utils import secure_filename
from uuid import uuid4

from api.controllers.auth import token_required
from api.schemas.misc import UploadImageResponseSchema, UploadImageSchema
from application.interfaces.repositories.account import IUserAccountRepository
from application.interfaces.services.auth import IAuthProvider

# TODO: refactor this mess: standardize image storing (single type), image scaling, etc.

ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def create_misc_blueprint(
    auth_provider: IAuthProvider, account_repository: IUserAccountRepository
):
    bp = APIBlueprint("misc", __name__)

    @bp.route("/images/<string:image_id>", methods=["GET"])
    @bp.output(FileSchema(), content_type="image/*")
    def get_image(image_id: str):
        response = send_from_directory(
            f"{current_app.config['APPLICATION_STATIC_DIR']}/images", image_id
        )
        return response

    @bp.route("/images", methods=["POST"])
    @bp.doc(security=[{"TwitchJWTAuth": []}])
    @bp.input(UploadImageSchema, location="files")
    @bp.output(UploadImageResponseSchema, 201)
    @token_required(auth_provider=auth_provider, account_repository=account_repository)
    def upload_image(files_data):
        file = files_data["file"]

        if not file.filename:
            return abort(400, "No selected file")

        if allowed_file(file.filename):
            file_id = str(uuid4())
            filename = secure_filename(file.filename)
            filename = f"{file_id}{filename}"
            file.save(
                os.path.join(
                    current_app.config["APPLICATION_STATIC_DIR"], "images", filename
                )
            )
            return {"id": filename}
        else:
            return abort(400, "Not allowed file format")

    return bp
