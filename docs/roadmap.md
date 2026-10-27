# AI Chat — Roadmap y estado del proyecto

## Resumen general

Este repositorio está orientado a construir un chat de IA full-stack con una base sólida en backend, una interfaz ligera en frontend y una evolución gradual hacia una aplicación más robusta en producción.

La estrategia actual es clara: primero validar la funcionalidad real del sistema, después añadir persistencia, streaming, contenedores, integración con IA y finalmente automatización y despliegue cloud.

La arquitectura actual del proyecto se compone de:

- Backend con FastAPI
- Frontend con React + Vite
- Base de datos PostgreSQL
- Integración con Ollama o un LLM compatible
- Contenedores con Docker Compose
- Evolución futura hacia CI/CD y Azure

---

## Milestones completados: resumen histórico

### Milestone 1 — Base del backend

Se estableció la base técnica del proyecto:

- creación del repositorio
- estructura inicial del monorepo
- entorno virtual de Python
- instalación de FastAPI y Uvicorn
- creación de `requirements.txt`
- implementación de la aplicación principal
- documentación Swagger en `/docs`

También se añadió el primer health check:

- `GET /health` devuelve `{"status": "ok"}`
- test automatizado validando el endpoint

### Milestone 2 — Estructura del backend

Se definió una organización limpia que separa responsabilidades:

- `api/routes/` → endpoints HTTP
- `services/` → lógica de negocio
- `core/` → configuración y utilidades
- `models/` y `dataaccess/` → persistencia
- `tests/` → validación funcional

La idea era mantener una arquitectura simple y clara, sin introducir complejidad innecesaria antes de tener funcionalidad real.

### Milestone 3 — POST /api/chat

Se implementó el primer endpoint de chat con contrato estable:

```json
{
  "message": "¿Qué es Docker?",
  "conversation_id": null
}
```

Respuesta inicial:

```json
{
  "response": "Has dicho: ¿Qué es Docker?"
}
```

Esto permitió validar:

- validación automática con Pydantic
- endpoint funcional con FastAPI
- tests básicos del API
- flujo inicial del chat sin IA aún integrada

### Milestone 4 — Integración con LLM local

Se decidió conectar el backend a un servidor Ollama externo en la red local, en lugar de depender de una instalación local del modelo.

Objetivo principal:

- comprobar conectividad a Ollama
- listar modelos disponibles
- elegir uno para desarrollo
- configurar la URL del modelo y el nombre del modelo en variables de entorno
- sustituir la respuesta simulada por una respuesta real del LLM

Se implementó el cliente de Ollama y se mantuvo el contrato del endpoint sin romper compatibilidad.

### Milestone 5 — Conversaciones persistentes

Con el LLM ya operativo, se añadió memoria conversacional:

- creación y recuperación de conversaciones
- modelo `Conversation`
- modelo `Message`
- almacenamiento en PostgreSQL
- migraciones con Alembic
- guardado de mensajes del usuario y del asistente
- recuperación del historial para dar contexto al LLM

Esto fue un cambio clave porque el sistema dejó de ser una simple IA sin memoria y pasó a mantener conversaciones reales.

### Milestone 6 — Streaming de respuestas

Se implementó streaming desde el modelo hasta el frontend para que la respuesta aparezca progresivamente en lugar de esperarse completamente.

Flujo:

```text
LLM
  ↓
token
ChatService
  ↓
FastAPI
  ↓
Frontend
```

Esto mejoró la experiencia de usuario y preparó la API para una interfaz más moderna y reactiva.

### Milestone 7 — Frontend básico

Se construyó una pequeña interfaz de chat para poder probar la API de forma visual, desde un navegador, sin necesidad de usar Swagger únicamente.

Incluía:

- listado de conversaciones
- creación de nuevas conversaciones
- envío de mensajes
- recepción de respuestas
- manejo básico del estado del chat

### Milestone 8 — Docker Compose

Se montó la aplicación con una configuración local utilizando Docker Compose:

- PostgreSQL en un contenedor
- backend en FastAPI
- frontend en Vite
- entorno compartido con variables de entorno

Esto permitió ejecutar el proyecto completo de forma reproducible y simplificó el onboarding del equipo.

---

## Milestone 9 — Web Search

Se añadieron tool_calls (web_search) con DDGS para que el modelo pueda consultar en internet, tanto en mensajes normales como en streaming.

---

## Milestone 10 — CI/CD

Se han creado workflow para validar los cambios y publicar las imagenes de forma autmática.
También se ha añadido el release drafter para poder generar las release-notes a partir de los commits/prs automaticamente.

---

## Milestone 11 - Mover BBDD a carpeta a parte

### Objetivo

Actualmente el proyecto de persistencia en alembic vive en la misma carpeta que el backend. Se ha decidido mover la BBDD a una carpeta separada, con todo lo necesario para que pueda ser ejecutado a parte.

### Tareas previstas

- [ ] Crear carpeta nueva para la BBDD.
- [ ] Crear entorno de desarrollo para el proyecto de persistencia.
- [ ] Limpiar el entorno de backend de las dependencias exclusivas del entorno de persistencia.
- [ ] Repasar Dockerfiles y compose.

---

## Milestone 12 — Securización backend

### Objetivo

Antes de publicar la aplicación en internet hay que securizarla y implementar mecanismos de control para protegerla de usos indebidos.

### Tareas previstas

- [ ] Implementar autenticación y autorización con Github.
- [ ] Proteger endpoints endpoints de la aplicación con la autorización.
- [ ] Forzar HTTPS.
- [ ] Cookies y protección CSRF.
- [ ] Implementar CORS para mi frontend.
- [ ] Implementar rate limiting.
- [ ] Límites de uso en el chat y en el web_search.
- [ ] Mover todos los secretos fuera del código.
- [ ] Añadir logs sin información sensible.

--- 

## Milestone 13 - Mejoras frontend

### Objetivo

Alinear el frontend con los cambios de securización del backend y otras correcciones importantes.

### Tareas previstas

- [ ] Añadir login, logout y gestión de sesión
- [ ] Renderizado de markdown de los mensajes
- [ ] Corregir funcionalidad de generar titulo
- [ ] HTTPS, cookies, CORS y CSRF
- [ ] Eliminar secretos y quitar persistencia del navegador si hay.
- [ ] CSP, auditoria de dependencias
- [ ] Configuración de producción

---

## Milestone 14 — Azure

### Objetivo

Desplegar la aplicación de forma accesible desde Internet y preparar la infraestructura base para un entorno real.

### Tareas previstas

- [ ] Crear resource group
- [ ] Elegir servicio de ejecución para la aplicación
- [ ] Desplegar backend en Azure
- [ ] Configurar variables y secretos
- [ ] Configurar base de datos gestionada
- [ ] Configurar logs y monitorización
- [ ] Comprobar disponibilidad de la aplicación desplegada
- [ ] Conectar CI/CD con Azure

### Opciones técnicas

Dependiendo del enfoque final, se podría usar:

- Azure App Service
- Azure Container Apps
- Azure Container Instances o AKS para una infraestructura más compleja

### Objetivo final

Tener una versión operativa del proyecto publicada en la nube, accesible para pruebas y validación real.

---

## Milestone 12 — Hardening y preparación para producción

Una vez que el backend, frontend, LLM y despliegue estén funcionando, el siguiente salto será reforzar la calidad operativa del sistema.

### Objetivos

- mejorar trazabilidad y logs
- manejar errores y fallbacks
- revisar seguridad básica
- definir timeouts y reintentos
- preparar observabilidad

### Tareas sugeridas

- [ ] Añadir logging estructurado
- [ ] Mejorar manejo de errores del LLM
- [ ] Añadir timeouts y reintentos
- [ ] Revisar configuración por entorno
- [ ] Documentar variables de entorno y secretos
- [ ] Añadir health checks más robustos

---

## Definition of Done — Proyecto MVP

El MVP del proyecto se considerará completo cuando:

- [x] FastAPI funcionando correctamente
- [x] `GET /health` operativo
- [x] `POST /api/chat` funcionando
- [x] LLM local o remoto integrado
- [x] Conversaciones persistentes
- [x] PostgreSQL configurado y operativo
- [x] Streaming implementado
- [x] Web Search funcionando
- [x] Tests básicos pasando
- [x] Docker Compose preparado
- [x] CI/CD básico activo
- [ ] Aplicación desplegada en Azure
