import os
from flask import Blueprint, current_app, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from uuid import uuid4

# TODO: refactor this mess

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_misc_blueprint():
    bp = Blueprint("misc", __name__)

    @bp.route("/images/<string:image_id>", methods=["GET"])
    def get_image(image_id: str):
        response = send_from_directory(
            current_app.config["APPLICATION_STATIC_DIR"], image_id
        )
        return response
    
    @bp.route('/images', methods=['POST'])
    def upload_image():
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        
        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        if file and allowed_file(file.filename):
            file_id = str(uuid4())
            filename = secure_filename(file.filename)
            filename = f'{file_id}{filename}'
            file.save(os.path.join(current_app.config['APPLICATION_STATIC_DIR'], 'images', filename))
            return jsonify({'id': filename}), 201

    return bp
