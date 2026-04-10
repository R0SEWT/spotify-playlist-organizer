from flask import session, current_app
from .spotify import SpotifyClient, SpotifyAuth


def get_spotify_client() -> SpotifyClient | None:
    """Crea un SpotifyClient con el token de la sesión del usuario actual."""
    user = session.get("user")
    if not user or not user.get("token"):
        return None
    auth: SpotifyAuth = current_app.config["spotify_auth"]
    return SpotifyClient(
        token=user["token"],
        refresh_token=user.get("refresh_token", ""),
        auth=auth,
    )
