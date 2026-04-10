from flask import Flask
from secrets import token_hex
from os import getenv

from .spotify import SpotifyAuth
from .db import create_conetion_db

from dotenv import load_dotenv

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token_hex(16)
    app.config["spotify_auth"] = SpotifyAuth(
        getenv("CLIENT_ID"),
        getenv("CLIENT_SECRET"),
        getenv("SCOPE"),
        getenv("REDIRECT_URI"),
    )

    create_conetion_db()

    from .auth import auth_routes
    from .public import public_routes
    from .user import user_routes

    app.register_blueprint(auth_routes)
    app.register_blueprint(public_routes)
    app.register_blueprint(user_routes)

    return app
