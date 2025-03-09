from datetime import datetime
from zoneinfo import ZoneInfo

from ulid import ULID


def current_datetime_utc():
    return datetime.now(ZoneInfo("UTC"))


def ulid_from_datetime_utc():
    now = current_datetime_utc()
    return str(ULID.from_datetime(now))
