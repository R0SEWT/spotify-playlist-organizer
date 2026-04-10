import requests
from spotipy import Spotify, SpotifyException
from functools import wraps
from typing import Optional


class TokenExpiredError(Exception):
    """Señal interna para que el decorador renueve el token y reintente."""


def renew_token_if_needed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except SpotifyException as e:
            if e.http_status == 401:
                self.renovar_token()
                return func(self, *args, **kwargs)
            raise
        except TokenExpiredError:
            self.renovar_token()
            return func(self, *args, **kwargs)
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
        if not result:
            return
        self.token = result["access_token"]
        self.refresh_token = result.get("refresh_token", self.refresh_token)
        self._client = Spotify(auth=self.token)

        # Propagar a la sesión para que el próximo request arranque con el token nuevo.
        try:
            from flask import session, has_request_context
            if has_request_context():
                user = session.get("user")
                if isinstance(user, dict):
                    user["token"] = self.token
                    user["refresh_token"] = self.refresh_token
                    session["user"] = user
        except RuntimeError:
            pass

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
                "img": _pick_image_url(item.get("album", {}).get("images", [])),
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
        if res.status_code == 401:
            raise TokenExpiredError()
        if res.status_code != 200:
            return []

        info_artistas = []
        for data in res.json().get("tracks", []):
            img_url = _pick_image_url(data.get("album", {}).get("images", []), min_height=300)
            for artista in data.get("artists", []):
                info_artistas.append({
                    "id": artista.get("id"),
                    "name": artista.get("name"),
                    "link": artista.get("external_urls", {}).get("spotify", ""),
                    "img": img_url,
                })
        return info_artistas


def _pick_image_url(images: list, min_height: int = 0) -> str:
    """Devuelve la URL de una imagen segura; prefiere una con height >= min_height."""
    if not images:
        return ""
    for img in images:
        if img.get("height", 0) >= min_height:
            return img.get("url", "")
    return images[0].get("url", "")
