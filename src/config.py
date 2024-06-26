import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    APPLICATION_HOST = os.getenv("APPLICATION_HOST")
    APPLICATION_ROOT = "/api"
    # TODO: deal with processing static files
    APPLICATION_STATIC_DIR = "/home/marcie/projects/event-hub-backend/static"

    TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
    TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
    TWITCH_REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")
