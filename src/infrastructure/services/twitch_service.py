import requests
from typing import Optional
from application.interfaces.services.twitch_service import ITwitchService
from infrastructure.dto.twitch_dto import (
    TwitchAuthToken,
    TwitchUserDTO,
)


class TwitchService(ITwitchService):
    BASE_AUTH_URL = "https://id.twitch.tv/oauth2/token"
    BASE_API_URL = "https://api.twitch.tv/helix"

    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._grant_type = "client_credentials"

        self._token: Optional[TwitchAuthToken] = None

    def _fetch_app_access_token(self) -> TwitchAuthToken:
        response = requests.post(
            self.BASE_AUTH_URL,
            data={
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "grant_type": "client_credentials",
            },
        )
        response.raise_for_status()
        token_data = response.json()
        return TwitchAuthToken(
            access_token=token_data["access_token"],
            expires_in=token_data["expires_in"],
            token_type=token_data["token_type"],
        )

    def _get_token(self) -> str:
        if self._token is None:
            self._token = self._fetch_app_access_token()
        return self._token.access_token

    def _auth_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._get_token()}",
            "Client-Id": self._client_id,
        }

    def _call_get_users(self, ids: list[str]) -> list[TwitchUserDTO]:
        params = {"id": ids}
        resp = requests.get(
            f"{self.BASE_API_URL}/users", params=params, headers=self._auth_headers()
        )
        resp.raise_for_status()
        data = resp.json().get("data", [])

        return [
            TwitchUserDTO(
                id=user_data["id"],
                display_name=user_data["display_name"],
                avatar_url=user_data["profile_image_url"],
            )
            for user_data in data
        ]

    def get_user_by_id(self, twitch_id: str) -> Optional[TwitchUserDTO]:
        result = next(iter(self._call_get_users(ids=[twitch_id])), None)
        return result

    def list_users_by_ids(self, twitch_ids: list[str]) -> list[TwitchUserDTO]:
        results = []
        for batch in (twitch_ids[i : i + 100] for i in range(0, len(twitch_ids), 100)):
            users_batch = self._call_get_users(batch)
            results.extend(users_batch)
        return results
