import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    APPLICATION_HOST = os.getenv("APPLICATION_HOST")
    APPLICATION_ROOT = "/api"
    # TODO: deal with processing static files
    APPLICATION_STATIC_DIR = "static"

    TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
    TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
    TWITCH_REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")

    DB_DRIVER = os.getenv("DB_DRIVER", "")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "")
    DB_NAME = os.getenv("DB_NAME")
