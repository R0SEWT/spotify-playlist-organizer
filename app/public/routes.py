from flask import Blueprint, render_template, request
from ..spotify import get_spotify_client
from ..algoritmo import recomendacion

public_routes = Blueprint('public', __name__)


@public_routes.get("/")
def index():
    client = get_spotify_client()
    artistas = client.obtener_artistas() if client else []
    tracks = client.user_top_tracks(8) if client else []
    return render_template('index.html', artistas=artistas, tracks=tracks)


@public_routes.get("/top")
def get_top_tracks():
    client = get_spotify_client()
    if not client:
        return [], 401
    return client.user_top_tracks(5) or []


@public_routes.get("/escuchar/<string:id>")
def escuchar(id):
    client = get_spotify_client()
    if not client:
        return "No autenticado", 401
    cancion: dict = client.obtener_cancion(id)

    uri = cancion["uri"]
    title = cancion.get("name")
    duration = cancion.get("duration_ms")
    images = cancion.get("album", {}).get("images", []) or []
    url_img = (images[1] if len(images) > 1 else images[0] if images else {}).get("url", "")
    artistas = map(lambda a: a["name"], cancion.get("artists", [{}]))

    return render_template('reproductor.html', id=id, uri=uri, title=title, artistas=list(artistas), duration=duration, url_img=url_img)


@public_routes.post("/recomendar")
def recomendar():
    client = get_spotify_client()
    if not client:
        return "No autenticado", 401

    data = request.get_json(silent=True) or {}
    historial = data.get("historial")
    nombre_cancion = data.get("nombre_cancion")
    artista = data.get("artista")
    if not nombre_cancion or not artista:
        return "Faltan campos requeridos", 400

    df_user = recomendacion.crear_df_user(historial)
    res_recomendacion = recomendacion.get_best_recommendations(nombre_cancion, artista, recomendacion.matriz_similaridad, df_user)

    URIs = res_recomendacion[:, -1]
    canciones = client.obtener_info_canciones(URIs)

    return [
        {
            "id": item["id"],
            "title": item['name'],
            "artist": item['artists'][0]['name'],
            "uri": item["uri"],
            "img": item["album"]["images"][-1]["url"],
            "duration": item["duration_ms"],
        }
        for item in canciones["tracks"]
    ]


@public_routes.get("/buscar")
def buscar():
    args = request.args
    query = args.get("q")

    client = get_spotify_client()
    if not query or not client:
        return render_template('busqueda.html', canciones=[])

    res = client.buscar_cancion(query)
    canciones = (
        {
            "id": track["id"],
            "title": track["name"],
            "img": track["album"]["images"][0]["url"],
            "duration": track["duration_ms"],
            "artist": [artist["name"] for artist in track["artists"]],
        }
        for track in res["tracks"]["items"]
    )
    return render_template('busqueda.html', canciones=canciones)
