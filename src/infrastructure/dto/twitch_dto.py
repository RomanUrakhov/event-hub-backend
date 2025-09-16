from dataclasses import dataclass


@dataclass
class TwitchUserDTO:
    id: str
    display_name: str
    avatar_url: str


@dataclass
class TwitchAuthToken:
    access_token: str
    expires_in: int
    token_type: str
