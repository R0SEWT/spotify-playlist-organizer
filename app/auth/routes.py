from flask import Blueprint, render_template, current_app, session, request, redirect
from ..spotify import SpotifyAuth
from .controlador import AuthCtrl
from ..decorators import no_login_required

auth_routes = Blueprint('auth', __name__)


@auth_routes.get("/login")
@no_login_required
def html_login():
    return render_template("login.html")


@auth_routes.get("/login-spotify")
@no_login_required
def login():
    auth: SpotifyAuth = current_app.config["spotify_auth"]
    return {"url": auth.get_url_oauth()}


@auth_routes.post("/logining")
@no_login_required
def callback():
    auth: SpotifyAuth = current_app.config["spotify_auth"]
    redirect_uri = (request.host_url + "login").replace("http://", "https://")

    data = request.get_json(silent=True) or {}
    code = data.get("code")
    code_verifier = data.get("codeVerifier")
    if not code or not code_verifier:
        return {"status": False, "error": "missing code or codeVerifier"}, 400

    data_token = auth.obtener_token(code, code_verifier, redirect_uri_override=redirect_uri)
    if not data_token:
        return {"status": False}

    token = data_token["access_token"]
    refresh_token = data_token["refresh_token"]

    from ..spotify import SpotifyClient
    client = SpotifyClient(token, refresh_token, auth)
    current_user = client.info_usuario()

    username = current_user["display_name"]
    user_id = current_user["id"]
    uri = current_user["uri"]
    img = current_user["images"][0]["url"] if current_user.get("images") else ""

    AuthCtrl.login(username, user_id, uri, img)

    session["user"] = {
        "username": username,
        "id": user_id,
        "uri": uri,
        "img": img,
        "token": token,
        "refresh_token": refresh_token,
    }
    return {"status": True}


@auth_routes.get("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
