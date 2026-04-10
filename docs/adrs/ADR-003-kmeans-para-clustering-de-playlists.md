# ADR-003: K-means para clustering de liked songs en playlists

- **Estado**: aceptado
- **Fecha**: 2026-04-09
- **Autor**: Rody Vilchez

## Contexto

El objetivo principal del proyecto es agrupar las liked songs del usuario en playlists tematicas automaticamente. El EDA en `eda/clasificador.ipynb` exploro este problema con 571 canciones y sus audio features + generos.

## Decision

Usar K-means con el siguiente pipeline:
1. Audio features normalizadas con StandardScaler
2. Generos vectorizados con TF-IDF
3. Reduccion de dimensionalidad con PCA (37 componentes, 75% varianza)
4. K-means con k=5, inicializacion k-means++, algoritmo Elkan

## Alternativas consideradas

### DBSCAN / HDBSCAN
- Pros: No requiere definir k, detecta clusters de forma arbitraria, maneja outliers
- Contras: Mas sensible a parametros (epsilon, min_samples), menos predecible en numero de playlists resultantes

### Solo audio features (sin generos)
- Pros: Menos dimensiones, menos ruido
- Contras: Pierde informacion semantica que agrupa artistas del mismo genero

## Consecuencias

- El EDA mostro desbalance severo: cluster 3 contiene 89.8% de las canciones (513/571). Esto sugiere que el pipeline con generos TF-IDF domina el clustering por proximidad semantica de nacionalidades/generos, no por audio features
- **Accion pendiente**: Experimentar con solo audio features o ajustar el peso relativo de generos vs features antes de integrar en la app (ver PLAN-001 Fase 2.2)
- K-means asume clusters esfericos — puede no capturar bien grupos con formas irregulares en el espacio de audio features
