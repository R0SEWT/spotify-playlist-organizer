# Docs as Code

Documentacion tecnica del proyecto, versionada junto al codigo.

## Estructura

```
docs/
  plans/       # Planes de implementacion y roadmaps
  adrs/        # Architecture Decision Records
```

## Convenciones

### Plans

Documentan que se va a hacer y por que. Formato:

- `PLAN-NNN-titulo.md`
- Incluyen: contexto, fases, orden de ejecucion
- Estados: `propuesto`, `en-progreso`, `completado`, `descartado`

### ADRs

Registran decisiones arquitectonicas importantes. Formato:

- `ADR-NNN-titulo.md`
- Basado en [Michael Nygard's template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- Estados: `propuesto`, `aceptado`, `deprecado`, `reemplazado`
- Un ADR nunca se borra, solo se marca como deprecado/reemplazado con referencia al nuevo
