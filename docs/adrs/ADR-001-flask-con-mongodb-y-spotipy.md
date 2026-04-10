# ADR-001: Flask con MongoDB y Spotipy como stack base

- **Estado**: aceptado
- **Fecha**: 2026-04-09
- **Autor**: Rody Vilchez

## Contexto

Se necesitaba una app web que interactúe con la API de Spotify para organizar canciones en playlists usando algoritmos de ML. El proyecto es personal/académico, con un solo desarrollador.

## Decisión

- **Backend**: Flask con blueprints (auth, public, user)
- **Base de datos**: MongoDB vía MongoEngine (modelos: Usuario, Favoritos, Historial, Playlist)
- **Spotify API**: Spotipy como wrapper, con autenticación OAuth2
- **Frontend**: Jinja2 templates + Tailwind CSS
- **ML**: scikit-learn (K-means, cosine similarity) + pandas

## Alternativas consideradas

### Django + PostgreSQL
- Pros: ORM más maduro, admin panel gratis
- Contras: Overhead para un proyecto con schema flexible (audio features varían), más opinionado

### FastAPI + MongoDB
- Pros: Async nativo, documentación automática de API
- Contras: Al momento del inicio del proyecto, Flask era más familiar y el frontend es server-rendered (Jinja2), no SPA

## Consecuencias

- MongoDB es bueno para documentos flexibles (audio features, metadata de canciones) pero no tiene relaciones fuertes
- MongoEngine da estructura con modelos tipo ORM
- Flask es ligero pero requiere más setup manual (blueprints, sesiones, error handling)
- Spotipy simplifica la interacción con Spotify pero tiene limitaciones en manejo de tokens multi-usuario
