# Docs as Code

Documentación técnica del proyecto, versionada junto al código.

## Estructura

```
docs/
  plans/       # Planes de implementación y roadmaps
  adrs/        # Architecture Decision Records
```

## Convenciones

### Plans

Documentan qué se va a hacer y por qué. Formato:

- `PLAN-NNN-título.md`
- Incluyen: contexto, fases, orden de ejecución
- Estados: `propuesto`, `en-progreso`, `completado`, `descartado`

### ADRs

Registran decisiones arquitectónicas importantes. Formato:

- `ADR-NNN-título.md`
- Basado en [Michael Nygard's template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- Estados: `propuesto`, `aceptado`, `deprecado`, `reemplazado`
- Un ADR nunca se borra, solo se marca como deprecado/reemplazado con referencia al nuevo
