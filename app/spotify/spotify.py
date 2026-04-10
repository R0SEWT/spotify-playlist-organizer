import requests
from spotipy import Spotify, SpotifyException
from functools import wraps
from typing import Optional


def renew_token_if_needed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except SpotifyException as e:
            if e.http_status == 401:
                self.renovar_token()
                return func(self, *args, **kwargs)
            else:
                raise
    return wrapper


class SpotifyAuth:
    """
    Maneja la configuración OAuth de Spotify (client_id, secret, scopes).
    No guarda tokens — esos viven en la sesión de cada usuario.
    """
    TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id: str, client_secret: str, scope: str, redirect_uri: str) -> None:
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.scope = scope
        self.redirect_uri = redirect_uri

    @property
    def client_id(self):
        return self.__client_id

    def get_url_oauth(self):
        return f"https://accounts.spotify.com/authorize?client_id={self.__client_id}&scope={self.scope}&response_type=code"

    def obtener_token(self, code, code_verifier, redirect_uri_override=None):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": self.__client_id,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri_override or self.redirect_uri,
            "code_verifier": code_verifier,
        }
        res = requests.post(self.TOKEN_ENDPOINT, data=data, headers=headers)
        if res.status_code != 200:
            return None
        return res.json()

    def refresh_access_token(self, refresh_token: str) -> Optional[dict]:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": self.__client_id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        res = requests.post(self.TOKEN_ENDPOINT, data=data, headers=headers)
        return res.json() if res.status_code == 200 else None


class SpotifyClient:
    """
    Cliente Spotify por usuario. Se crea con el token de la sesión.
    """

    def __init__(self, token: str, refresh_token: str, auth: SpotifyAuth) -> None:
        self.token = token
        self.refresh_token = refresh_token
        self._auth = auth
        self._client = Spotify(auth=token)

    def renovar_token(self):
        result = self._auth.refresh_access_token(self.refresh_token)
        if result:
            self.token = result["access_token"]
            self.refresh_token = result.get("refresh_token", self.refresh_token)
            self._client = Spotify(auth=self.token)

    @renew_token_if_needed
    def info_usuario(self):
        return self._client.current_user()

    @renew_token_if_needed
    def buscar_cancion(self, nombre):
        return self._client.search(nombre, limit=10)

    @renew_token_if_needed
    def user_top_tracks(self, top):
        top_tracks = self._client.current_user_top_tracks(time_range='short_term', limit=top)
        return [
            {
                "id": item["id"],
                "title": item['name'],
                "artist_name": item['artists'][0]['name'],
                "uri": item["uri"],
                "img": item["album"]["images"][1]["url"],
            }
            for item in top_tracks['items']
        ]

    @renew_token_if_needed
    def obtener_cancion(self, id):
        return self._client.track(id)

    @renew_token_if_needed
    def obtener_info_canciones(self, q: list):
        return self._client.tracks(q)

    @renew_token_if_needed
    def obtener_artistas(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        res = requests.get(
            "https://api.spotify.com/v1/recommendations?limit=8&seed_genres=anime,pop,raggeton,j-pop",
            headers=headers,
        )
        if res.status_code != 200:
            return []

        info_artistas = []
        for data in res.json()["tracks"]:
            images = data.get("album", {}).get("images", [{}])
            img = list(filter(lambda img: img["height"] >= 300, images))[0]
            data_artista = data["artists"]
            info_artistas += [
                {
                    "id": artista["id"],
                    "name": artista["name"],
                    "link": artista["external_urls"]["spotify"],
                    "img": img.get("url", ""),
                }
                for artista in data_artista
            ]
        return info_artistas
