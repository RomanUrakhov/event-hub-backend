from flask import Blueprint


def create_misc_blueprint():
    bp = Blueprint("misc", __name__)

    @bp.route("/images/<string:id>", methods=["GET"])
    def get_image(id: str):
        return (
            "https://i.kym-cdn.com/entries/icons/facebook/000/042/690/Screen_Shot_2022-11-16_at_2.24.03_PM.jpg",
            200,
        )

    return bp
