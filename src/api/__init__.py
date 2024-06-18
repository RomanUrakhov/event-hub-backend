from datetime import date
from flask import Flask

from infrastructure.dao.event import InMemoryEventDAO
from src.config import Config
from src.infrastructure.repositories.event import InMemoryEventRepository
from src.domain.models.event import Event


def create_app() -> Flask:
    app = Flask(__name__)

    config = Config()
    app.config.from_object(config)

    _register_blueprints(app)

    return app


def _register_blueprints(app: Flask):
    from .controllers.event import create_event_blueprint
    from .controllers.misc import create_misc_blueprint

    # TODO: find the way to setup global API prefix at once and not duplicate for every blueprint
    event_bp = create_event_blueprint(
        event_repo=InMemoryEventRepository(
            [
                Event(
                    id="123",
                    name="tst",
                    start_date=date.fromisoformat("2024-05-24"),
                    end_date=date.fromisoformat("2024-05-30"),
                    description=None,
                    additional_links=[],
                )
            ]
        ),
        event_dao=InMemoryEventDAO(),
    )
    app.register_blueprint(event_bp, url_prefix=app.config["APPLICATION_ROOT"])

    misc_bp = create_misc_blueprint()
    app.register_blueprint(misc_bp, url_prefix=app.config["APPLICATION_ROOT"])

    return app
