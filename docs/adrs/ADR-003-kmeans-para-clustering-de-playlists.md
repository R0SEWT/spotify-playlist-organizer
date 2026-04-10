# ADR-003: K-means para clustering de liked songs en playlists

- **Estado**: aceptado
- **Fecha**: 2026-04-09
- **Autor**: Rody Vilchez

## Contexto

El objetivo principal del proyecto es agrupar las liked songs del usuario en playlists temáticas automáticamente. El EDA en `eda/clasificador.ipynb` exploró este problema con 571 canciones y sus audio features + géneros.

## Decisión

Usar K-means con el siguiente pipeline:
1. Audio features normalizadas con StandardScaler
2. Géneros vectorizados con TF-IDF
3. Reducción de dimensionalidad con PCA (37 componentes, 75% varianza)
4. K-means con k=5, inicialización k-means++, algoritmo Elkan

## Alternativas consideradas

### DBSCAN / HDBSCAN
- Pros: No requiere definir k, detecta clusters de forma arbitraria, maneja outliers
- Contras: Más sensible a parámetros (epsilon, min_samples), menos predecible en número de playlists resultantes

### Solo audio features (sin géneros)
- Pros: Menos dimensiones, menos ruido
- Contras: Pierde información semántica que agrupa artistas del mismo género

## Consecuencias

- El EDA mostró desbalance severo: cluster 3 contiene 89.8% de las canciones (513/571). Esto sugiere que el pipeline con géneros TF-IDF domina el clustering por proximidad semántica de nacionalidades/géneros, no por audio features
- **Acción pendiente**: Experimentar con solo audio features o ajustar el peso relativo de géneros vs features antes de integrar en la app (ver PLAN-001 Fase 2.2)
- K-means asume clusters esféricos — puede no capturar bien grupos con formas irregulares en el espacio de audio features
