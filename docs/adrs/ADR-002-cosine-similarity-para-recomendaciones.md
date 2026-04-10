# ADR-002: Cosine similarity sobre audio features para recomendaciones

- **Estado**: aceptado
- **Fecha**: 2026-04-09
- **Autor**: Rody Vilchez

## Contexto

La app necesita recomendar canciones similares a una dada. Se dispone de audio features de Spotify (danceability, energy, speechiness, acousticness, instrumentalness, valence, tempo) tanto en un dataset generico de 18K tracks como en las liked songs del usuario.

## Decision

Usar cosine similarity sobre 7 audio features numericas para encontrar canciones similares. Implementado en `app/algoritmo/recomendacion.py` con una matriz de similitud precalculada al iniciar la app.

## Alternativas consideradas

### Euclidean distance
- Pros: Intuitivo, simple
- Contras: Sensible a la escala de las features (tempo en BPM vs danceability 0-1). Requiere normalizacion obligatoria

### Modelo de embeddings (neural)
- Pros: Captura relaciones no lineales
- Contras: Requiere datos de entrenamiento masivos, overhead de infraestructura, no justificado para el volumen actual

## Consecuencias

- La matriz se calcula en import time sobre todo el CSV — funciona pero escala mal con datasets grandes
- Cosine similarity es invariante a la magnitud, lo que ayuda con features de distinta escala
- Las recomendaciones dependen de un CSV estatico generico, no de las canciones reales del usuario (ver PLAN-001 Fase 3.1 para mejora planificada)
