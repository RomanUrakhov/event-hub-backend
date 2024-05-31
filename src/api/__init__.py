from flask import Flask

from src.config import Config
from src.infrastructure.repositories.event import InMemoryEventRepository


def create_app() -> Flask:
    app = Flask(__name__)

    config = Config()
    app.config.from_object(config)

    _register_blueprints(app)

    return app


def _register_blueprints(app: Flask):
    from .controllers.event import create_event_blueprint
    from .controllers.misc import create_misc_blueprint

    event_bp = create_event_blueprint(event_repo=InMemoryEventRepository())
    app.register_blueprint(event_bp)

    misc_bp = create_misc_blueprint()
    app.register_blueprint(misc_bp)

    return app
