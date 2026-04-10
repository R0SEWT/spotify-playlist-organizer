# ADR-004: Render + MongoDB Atlas para deploy gratuito

- **Estado**: propuesto
- **Fecha**: 2026-04-09
- **Autor**: Rody Vilchez

## Contexto

Se necesita un deploy gratuito para portafolio/demo. La app usa Flask + MongoDB. Requisitos: $0/mes, URL publica, soporte para Python + MongoDB, deploy desde GitHub.

## Decision

- **App**: Render free tier (web service con Docker)
- **BD**: MongoDB Atlas free tier (M0, 512MB)
- **Cache**: Upstash Redis free tier (10K comandos/dia)
- **Server**: gunicorn en vez del dev server de Flask

## Alternativas consideradas

### Railway
- Pros: UX excelente, deploy rapido, MongoDB addon integrado
- Contras: Elimino el free tier en 2023. Requiere plan de $5/mes minimo

### Fly.io
- Pros: Edge computing, buen free tier para apps
- Contras: No tiene MongoDB managed — requiere correr Mongo en un volumen (fragil) o usar Atlas igual. Mas complejo de configurar

### Vercel
- Pros: Deploy instantaneo, excelente para frontend
- Contras: Serverless — Flask no es ideal. Cold starts largos con scikit-learn en memoria

## Consecuencias

- Render free duerme la app tras 15min de inactividad — primer request tarda ~30s en despertar. Aceptable para demo
- Atlas M0 tiene 512MB — suficiente para historial/favoritos de pocos usuarios
- gunicorn reemplaza al dev server de Flask para produccion
- Deploy automatico desde main via GitHub — cualquier push actualiza la app
