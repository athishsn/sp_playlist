import requests
import time
from typing import Dict, List

from ingestion.config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REFRESH_TOKEN,
    SPOTIFY_BASE_URL,
)

class SpotifyClient:

    def __init__(self) -> None:
        self.access_token = self._refresh_access_token()

    def _refresh_access_token(self) -> str:
        url = "https://accounts.spotify.com/api/token"

        data = {
            "grant_type": "refresh_token",
            "refresh_token": SPOTIFY_REFRESH_TOKEN,
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        }

        resp = requests.post(url, data=data, timeout=10)

        resp.raise_for_status()

        return resp.json()["access_token"]

    def _headers(self) -> Dict:
        return {"Authorization": f"Bearer {self.access_token}"}

    def get_recently_played(
        self,
        after_ts_ms: int | None = None,
        limit: int = 50,
    ) -> List[Dict]:

        params = {"limit": limit}
        if after_ts_ms:
            params["after"] = after_ts_ms

        url = f"{SPOTIFY_BASE_URL}/me/player/recently-played"

        resp = requests.get(url, headers=self._headers(), params=params, timeout=10)

        if resp.status_code == 401:
            self.access_token = self._refresh_access_token()
            resp = requests.get(url, headers=self._headers(), params=params, timeout=10)

        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 5))
            time.sleep(retry_after)
            return self.get_recently_played(after_ts_ms, limit)

        resp.raise_for_status()
        return resp.json().get("items", [])
