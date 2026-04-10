# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Spanish-language Flask web app that organizes Spotify liked songs into playlists using K-means clustering and cosine similarity-based recommendations. Users authenticate via Spotify OAuth, browse/search tracks, and get personalized recommendations based on audio features.

## Commands

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Tailwind (for CSS)
npm install

# Run the dev server
python index.py

# Build Tailwind CSS (watches templates in app/templates/ and app/static/js/)
npx tailwindcss -o app/static/css/output.css --watch
```

## Required Environment Variables

Set in `.env` (loaded via python-dotenv): `CLIENT_ID`, `CLIENT_SECRET`, `SPOTIFY_USERNAME`, `SCOPE`, `REDIRECT_URI`, `DB_NAME`, `URI_DB`.

## Architecture

**Entry point:** `index.py` calls `create_app()` from `app/app.py`, which initializes the Flask app, connects to MongoDB, and registers three blueprints.

**Blueprints (route modules):**
- `app/auth/` — Spotify OAuth login/logout, session management. Controller in `controlador.py`.
- `app/public/` — Homepage, search, song player, recommendation endpoint (`/recomendar`).
- `app/user/` — Favorites, listening history (requires auth via `before_request`).

**Key layers:**
- `app/spotify/spotify.py` — `SpotifyApi` class wrapping `spotipy`. Stored as `app.config["spotify_client"]` (single shared instance). Uses `@renew_token_if_needed` decorator for automatic token refresh on 401s.
- `app/algoritmo/recomendacion.py` — Recommendation engine using cosine similarity on audio features (Danceability, Energy, Speechiness, etc.) from `app/algoritmo/datasets/Spotify.csv`. Module-level globals (`df_musica`, `matriz_similaridad`) are computed at import time. Also has `filtro_colaborativo()` for user-based collaborative filtering.
- `app/db/` — MongoDB via MongoEngine. Models: `Usuario`, `Favoritos`, `Historial`, `Playlist`.
- `app/decorators/decorators.py` — `@no_login_required` redirects authenticated users away from login pages.

**Frontend:** Jinja2 templates in `app/templates/`, styled with Tailwind CSS. Static JS in `app/static/js/`.

**EDA:** `eda/` contains exploratory data analysis scripts (separate from the main app).

## Language

The codebase (variable names, comments, docstrings) is primarily in Spanish.
