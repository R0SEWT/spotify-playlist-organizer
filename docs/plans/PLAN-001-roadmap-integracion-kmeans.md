# PLAN-001: Roadmap - Integracion del clustering y mejoras generales

- **Estado**: propuesto
- **Fecha**: 2026-04-09
- **Autor**: Rody Vilchez

## Contexto

La app Flask tiene autenticacion Spotify, busqueda, reproductor, recomendaciones por cosine similarity, y historial/favoritos en MongoDB. En paralelo, el directorio `eda/` tiene trabajo maduro: extraccion de liked songs con audio features, clustering K-means (5 clusters con TF-IDF de generos + audio features), y creacion de playlists en Spotify. Sin embargo, nada del EDA esta integrado en la app web. El dataset de recomendaciones (`app/algoritmo/datasets/Spotify.csv`, 18K tracks) es estatico y generico, no usa los datos reales del usuario.

---

## Fase 1: Fundamentos (bugs criticos)

### 1.1 — SpotifyApi multi-usuario
- **Problema**: Hay una sola instancia de `SpotifyApi` en `app.config["spotify_client"]`. Si dos usuarios se logean, el token del segundo sobreescribe al primero.
- **Solucion**: Mover token/refresh_token a la sesion o a MongoDB (`Usuario`). Que cada request use el token de la sesion para crear/inicializar el cliente Spotify.
- **Archivos**: `app/app.py`, `app/spotify/spotify.py`, `app/auth/routes.py`, `app/public/routes.py`, `app/user/routes.py`

### 1.2 — Manejo de errores basico
- Reemplazar `print()` por `logging`
- Las rutas que hacen `except: return {"status": False}` ocultan bugs. Al menos loggear la excepcion.
- **Archivos**: `app/user/routes.py`, `app/spotify/spotify.py`

---

## Fase 2: Integrar el K-means del EDA en la app

### 2.1 — Extraer audio features del usuario en tiempo real
- Usar `spotify_client.audio_features()` de spotipy para obtener las features de las liked songs del usuario (como hace `eda/get_spotify_list.ipynb`).
- Cachear en MongoDB o Redis para no repetir llamadas.
- **Referencia**: `eda/get_spotify_list.ipynb` ya tiene la logica de extraccion batch + cache de generos en `artist_genre_cache.json`.

### 2.2 — Modulo de clustering
- Extraer la logica de `eda/clasificador.ipynb` a un modulo Python reutilizable (ej: `app/algoritmo/clustering.py`).
- Pipeline: normalizacion -> TF-IDF de generos -> PCA -> K-means.
- Permitir al usuario elegir numero de clusters o usar el elbow method automatico.
- **Nota**: El EDA mostro desbalance fuerte (cluster 3 = 89.8% de canciones). Considerar ajustar: usar solo audio features sin generos, o probar DBSCAN/HDBSCAN como alternativa.

### 2.3 — Crear playlists en Spotify desde la app
- Endpoint nuevo: `/crear-playlists` que ejecute el clustering y cree las playlists via API.
- Reusar logica de `eda/crear_playlist.ipynb` (batch add de 100 tracks).
- El modelo `Playlist` en `app/db/models/playlist.py` ya existe pero no se usa — conectarlo.

---

## Fase 3: Mejorar recomendaciones

### 3.1 — Recomendaciones basadas en datos del usuario
- Reemplazar el CSV estatico de 18K tracks por las audio features reales de las canciones del usuario.
- `recomendacion.py` ya tiene `get_best_recommendations()` y `filtro_colaborativo()` — adaptar para que trabajen con datos dinamicos en vez de globals de modulo.
- **Archivos**: `app/algoritmo/recomendacion.py`

### 3.2 — Filtro colaborativo funcional
- `filtro_colaborativo()` existe pero no se llama desde ninguna ruta.
- Necesita un DataFrame de usuarios x canciones que se construya desde MongoDB (`Historial`, `Favoritos`).
- Agregar endpoint `/recomendaciones-colaborativas`.

---

## Fase 4: Frontend y UX

### 4.1 — Vista de clusters
- Pagina donde el usuario vea sus canciones agrupadas por cluster con nombres descriptivos (basados en las caracteristicas dominantes del cluster).
- Boton "Crear playlist en Spotify" por cada cluster.

### 4.2 — Visualizacion
- Integrar la visualizacion 3D de PCA (como `eda/file5k.html` con Plotly) en la app para que el usuario vea sus clusters interactivamente.

---

## Fase 5: Infraestructura

### 5.1 — Tests
- Unit tests para `recomendacion.py` (funciones puras: `clean_data`, `get_similarities`, `filtro_colaborativo`).
- Integration tests para las rutas principales.

### 5.2 — Docker
- `docker-compose.yml` con Flask + MongoDB + Redis.

### 5.3 — Deploy
- Railway/Render/Fly.io con Spotify API en modo development.

---

## Orden sugerido de ejecucion

```
Fase 1.1 (multi-usuario) -> Fase 2.1 (audio features) -> Fase 2.2 (clustering module)
-> Fase 2.3 (crear playlists) -> Fase 3.1 (recomendaciones dinamicas)
-> Fase 4.1 (vista clusters) -> Fase 5 (tests, docker, deploy)
```

Las fases 1.2, 3.2, 4.2 y 5.x se pueden intercalar segun prioridad.
