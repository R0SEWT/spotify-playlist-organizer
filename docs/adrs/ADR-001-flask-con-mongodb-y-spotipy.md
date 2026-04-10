# ADR-001: Flask con MongoDB y Spotipy como stack base

- **Estado**: aceptado
- **Fecha**: 2026-04-09
- **Autor**: Rody Vilchez

## Contexto

Se necesitaba una app web que interactue con la API de Spotify para organizar canciones en playlists usando algoritmos de ML. El proyecto es personal/academico, con un solo desarrollador.

## Decision

- **Backend**: Flask con blueprints (auth, public, user)
- **Base de datos**: MongoDB via MongoEngine (modelos: Usuario, Favoritos, Historial, Playlist)
- **Spotify API**: Spotipy como wrapper, con autenticacion OAuth2
- **Frontend**: Jinja2 templates + Tailwind CSS
- **ML**: scikit-learn (K-means, cosine similarity) + pandas

## Alternativas consideradas

### Django + PostgreSQL
- Pros: ORM mas maduro, admin panel gratis
- Contras: Overhead para un proyecto con schema flexible (audio features varian), mas opinionado

### FastAPI + MongoDB
- Pros: Async nativo, documentacion automatica de API
- Contras: Al momento del inicio del proyecto, Flask era mas familiar y el frontend es server-rendered (Jinja2), no SPA

## Consecuencias

- MongoDB es bueno para documentos flexibles (audio features, metadata de canciones) pero no tiene relaciones fuertes
- MongoEngine da estructura con modelos tipo ORM
- Flask es ligero pero requiere mas setup manual (blueprints, sesiones, error handling)
- Spotipy simplifica la interaccion con Spotify pero tiene limitaciones en manejo de tokens multi-usuario
