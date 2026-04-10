# ADR-004: Render + MongoDB Atlas para deploy gratuito

- **Estado**: propuesto
- **Fecha**: 2026-04-09
- **Autor**: Rody Vilchez

## Contexto

Se necesita un deploy gratuito para portafolio/demo. La app usa Flask + MongoDB. Requisitos: $0/mes, URL pública, soporte para Python + MongoDB, deploy desde GitHub.

## Decisión

- **App**: Render free tier (web service con Docker)
- **BD**: MongoDB Atlas free tier (M0, 512MB)
- **Cache**: Upstash Redis free tier (10K comandos/día)
- **Server**: gunicorn en vez del dev server de Flask

## Alternativas consideradas

### Railway
- Pros: UX excelente, deploy rápido, MongoDB addon integrado
- Contras: Eliminó el free tier en 2023. Requiere plan de $5/mes mínimo

### Fly.io
- Pros: Edge computing, buen free tier para apps
- Contras: No tiene MongoDB managed — requiere correr Mongo en un volumen (frágil) o usar Atlas igual. Más complejo de configurar

### Vercel
- Pros: Deploy instantáneo, excelente para frontend
- Contras: Serverless — Flask no es ideal. Cold starts largos con scikit-learn en memoria

## Consecuencias

- Render free duerme la app tras 15min de inactividad — primer request tarda ~30s en despertar. Aceptable para demo
- Atlas M0 tiene 512MB — suficiente para historial/favoritos de pocos usuarios
- gunicorn reemplaza al dev server de Flask para producción
- Deploy automático desde main vía GitHub — cualquier push actualiza la app
