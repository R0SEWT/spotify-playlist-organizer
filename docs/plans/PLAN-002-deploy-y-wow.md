# PLAN-002: Despliegue gratuito + features efecto wow

- **Estado**: propuesto
- **Fecha**: 2026-04-09
- **Autor**: Rody Vilchez

**Objetivo**: Portafolio/demo con link vivo, costo $0, máximo impacto visual y funcional.

---

## Parte 1: Despliegue

### Infraestructura

| Servicio | Proveedor | Tier | Límites |
|----------|-----------|------|---------|
| App Flask | Render (web service) | Free | Sleep tras 15min inactividad, 750h/mes |
| MongoDB | MongoDB Atlas | Free (M0) | 512MB, cluster compartido |
| Redis (cache) | Upstash | Free | 10K comandos/día, 256MB |

### Archivos a crear

1. `Dockerfile` — Python 3.11-slim, gunicorn como server
2. `docker-compose.yml` — flask + mongo + redis para desarrollo local
3. `.dockerignore` — excluir eda/, node_modules/, .env, __pycache__
4. `render.yaml` — Infrastructure as Code para Render
5. Agregar `gunicorn` a `requirements.txt`

### Spotify API
- Agregar URL de Render a Redirect URIs en Spotify Developer Dashboard
- Development Mode: hasta 25 usuarios (suficiente para demo)

### Pasos
1. Crear cluster MongoDB Atlas free (M0)
2. Crear cuenta Render, conectar repo GitHub
3. Configurar env vars en Render
4. Configurar Redirect URI en Spotify Dashboard
5. Deploy automático desde main

---

## Parte 2: Features efecto wow

### Impacto alto + esfuerzo bajo

**UI estilo Spotify** — Dark theme (#1DB954 verde, #191414 fondo), cards con cover art, animaciones hover, transiciones CSS.

**Mood Ring** — Resumen visual tipo Spotify Wrapped con audio features promedio del usuario. "Tu música es 73% bailable". Gauges animados. Datos ya disponibles.

**One-click playlist creation** — Botón "Crear en Spotify" por cluster. Lógica ya existe en `eda/crear_playlist.ipynb`.

### Impacto alto + esfuerzo medio

**Visualización 3D de clusters** — Plotly.js scatter 3D, cada punto una canción coloreada por cluster. Hover muestra nombre + artista, click abre en Spotify. PCA 3 componentes. Ya explorado en `eda/file5k.html`.

**Radar chart por cluster** — Chart.js/Plotly mostrando perfil de audio features (danceability, energy, valence, etc). Comparar clusters lado a lado.

**Nombres de playlists con LLM** — Claude Haiku o reglas básicas. Input: artistas + features promedio + géneros. Output: nombre creativo + emoji + descripción.

### Impacto medio + esfuerzo medio

**Compatibilidad entre amigos** — Cosine similarity de perfiles de audio features entre usuarios. Compartible en redes.

---

## Verificación

1. `docker-compose up` levanta app + mongo localmente
2. Login con Spotify funciona con redirect a localhost
3. Deploy en Render: URL pública responde, login redirige correctamente
4. MongoDB Atlas conecta desde Render
