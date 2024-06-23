from datetime import date
from flask import Flask

from application.interfaces.dao.streamer import StreamerDetailsDTO, StreamerEventItem
from infrastructure.dao.event import InMemoryEventDAO
from infrastructure.dao.streamer import InMemoryStreamerDAO
from infrastructure.repositories.streamer import InMemoryStreamerRepository
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
    from .controllers.streamer import create_streamer_blueprint

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

    streamer_bp = create_streamer_blueprint(
        streamer_repository=InMemoryStreamerRepository([]),
        streamer_dao=InMemoryStreamerDAO(
            data=[
                StreamerDetailsDTO(
                    id="123",
                    twitch_id="123",
                    name="test",
                    events=[
                        StreamerEventItem(
                            id="123",
                            name="event-1",
                            start_date=date.fromisoformat("2024-05-05"),
                            end_date=date.fromisoformat("2024-05-10"),
                            image_id="123",
                        ),
                        StreamerEventItem(
                            id="456",
                            name="event-2",
                            start_date=date.fromisoformat("2024-06-05"),
                            end_date=date.fromisoformat("2024-06-10"),
                            image_id="456",
                        ),
                    ],
                )
            ]
        ),
    )
    app.register_blueprint(streamer_bp, url_prefix=app.config["APPLICATION_ROOT"])

    return app
