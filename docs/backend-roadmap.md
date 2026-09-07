# AI Chat — Backend MVP

## Objetivo del proyecto

Construir progresivamente un chat de IA full-stack que empiece como un MVP sencillo y evolucione durante el roadmap hacia una aplicación Cloud Native con IA, Azure, CI/CD, RAG, IaC y otras capacidades.

En esta primera iteración el objetivo es conseguir un backend funcional antes de añadir funcionalidades más avanzadas.

---

# Arquitectura actual

```text
ai-chat/
├── backend/
├── frontend/
├── docker-compose.yml
├── README.md
└── .gitignore
```

Por ahora estamos trabajando únicamente en `backend/`.

La idea es mantener backend y frontend en el mismo repositorio (monorepo).

---

# Milestone 1 — Base del backend

## Proyecto Python

- [x] Crear repositorio Git
- [x] Crear carpeta `backend/`
- [x] Crear carpeta `frontend/`
- [x] Crear entorno virtual con `venv`
- [x] Instalar FastAPI
- [x] Instalar Uvicorn
- [x] Crear `requirements.txt`
- [x] Crear aplicación FastAPI
- [x] Configurar `/docs` de Swagger

## Health check

- [x] Crear `GET /health`
- [x] Devolver `{"status": "ok"}`
- [x] Crear test del endpoint
- [x] Ejecutar tests con `pytest`

---

# Milestone 2 — Estructura del backend

Estructura actual prevista:

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py
│   │       └── chat.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── chat.py
│   │
│   └── services/
│       ├── __init__.py
│       └── chat.py
│
├── tests/
│   ├── test_health.py
│   └── test_chat.py
│
├── .env
├── .env.example
├── .gitignore
└── requirements.txt
```

## Separación de responsabilidades

- `api/routes/` → endpoints HTTP
- `schemas/` → modelos de entrada y salida
- `services/` → lógica de negocio
- `core/` → configuración

No se busca una arquitectura excesivamente compleja todavía. La idea es construir primero funcionalidades tangibles y refactorizar cuando sea necesario.

---

# Milestone 3 — POST /api/chat

## Contrato

Endpoint:

```text
POST /api/chat
```

Request:

```json
{
  "message": "¿Qué es Docker?",
  "conversation_id": null
}
```

Response actual:

```json
{
  "response": "Has dicho: ¿Qué es Docker?"
}
```

## Implementado

- [x] Crear `ChatRequest`
- [x] Crear `ChatResponse`
- [x] Crear `ChatService`
- [x] Crear `POST /api/chat`
- [x] Registrar router de chat en FastAPI
- [x] Validación automática mediante Pydantic
- [x] Añadir `conversation_id` al request como campo opcional
- [x] Crear test del endpoint
- [x] Probar endpoint mediante Swagger

## Estado actual

El endpoint todavía devuelve una respuesta simulada.

```text
POST /api/chat
      ↓
ChatService
      ↓
respuesta simulada
```

---

# Milestone 4 — Integrar LLM local

## Decisión tomada

Utilizar un servidor Ollama que ya está funcionando en otro ordenador de la red local.

No es necesario instalar Ollama en el ordenador donde se desarrolla el backend.

Arquitectura:

```text
┌─────────────────────┐
│ PC de desarrollo    │
│                     │
│ FastAPI             │
│ localhost:8000      │
└──────────┬──────────┘
           │
           │ LAN
           ▼
┌─────────────────────┐
│ Otro ordenador      │
│                     │
│ Ollama              │
│ :11434              │
│                     │
│ Modelo LLM          │
└─────────────────────┘
```

## Pendiente

- [x] Comprobar conectividad desde el PC de desarrollo a Ollama
- [x] Ejecutar `GET /api/tags` contra el servidor Ollama
- [x] Comprobar qué modelos están disponibles
- [x] Elegir modelo para desarrollo
- [x] Instalar dependencia cliente necesaria
- [x] Configurar URL de Ollama mediante `.env`
- [x] Configurar nombre del modelo mediante `.env`
- [x] Implementar cliente para Ollama
- [x] Modificar `ChatService` para utilizar el LLM real
- [x] Mantener `POST /api/chat` sin cambiar su contrato
- [x] Añadir tests del servicio con el LLM aislado/mockeado
- [x] Probar conversación real desde Swagger

## Configuración prevista

Ejemplo:

```env
OLLAMA_BASE_URL=http://IP_DEL_ORDENADOR:11434/v1
OLLAMA_MODEL=nombre-del-modelo
```

La URL y el modelo reales se decidirán después de comprobar el servidor Ollama.

---

# Milestone 5 — Conversaciones

Una vez funcionando el LLM:

```text
POST /api/chat
      ↓
ChatService
      ↓
LLM
      ↓
respuesta
```

añadir persistencia del contexto de conversación.

## Pendiente

- [x] Definir correctamente `conversation_id`
- [x] Crear modelo `Conversation`
- [x] Crear modelo `Message`
- [x] Añadir PostgreSQL
- [x] Añadir SQLAlchemy
- [x] Añadir Alembic
- [x] Crear migraciones
- [x] Guardar mensajes de usuario
- [x] Guardar respuestas del asistente
- [x] Recuperar historial
- [x] Enviar historial relevante al LLM
- [x] Endpoint para recuperar una conversación
- [x] Endpoint para crear/nueva conversación

Modelo inicial previsto:

```text
Conversation
-------------
id
created_at
updated_at

Message
-------------
id
conversation_id
role
content
created_at
```

No se implementará autenticación ni multiusuario todavía.

---

# Milestone 6 — Streaming

Objetivo: que la respuesta aparezca progresivamente en lugar de esperar a que el LLM genere todo el texto.

## Pendiente

- [ ] Comprobar streaming del modelo Ollama
- [ ] Implementar streaming en el cliente LLM
- [ ] Propagar streaming desde `ChatService`
- [ ] Crear respuesta streaming en FastAPI
- [ ] Manejar errores durante streaming
- [ ] Añadir tests
- [ ] Preparar contrato para que React pueda consumir el stream

Flujo:

```text
LLM
 ↓
token
 ↓
ChatService
 ↓
FastAPI
 ↓
Frontend
```

---

# Milestone 7 - Frontend básico

Objetivo: tener una pequeña interfaz simple para usar la API.

# Milestone 8 - Montar docker compose

Objetivo: Poder arrancar todo el proyecto dockerizado.

# Milestone 9 — Web Search

Objetivo: permitir que el modelo consulte Internet cuando necesite información actual.

## Arquitectura prevista

```text
                  User
                    │
                    ▼
               ChatService
                    │
                    ▼
                   LLM
                    │
             ┌──────┴──────┐
             │             │
          respuesta     web_search
                           │
                           ▼
                      SearchService
                           │
                           ▼
                       Search API
                           │
                           ▼
                          LLM
                           │
                           ▼
                       respuesta
```

## Pendiente

- [ ] Elegir proveedor de Web Search
- [ ] Crear `SearchService`
- [ ] Definir herramienta `web_search`
- [ ] Implementar tool/function calling
- [ ] Ejecutar búsquedas desde el backend
- [ ] Devolver resultados al LLM
- [ ] Incluir fuentes en la respuesta
- [ ] Añadir tests

---

# Milestone 8 — Docker

Todavía no es prioritario.

## Pendiente

- [ ] Crear Dockerfile del backend
- [ ] Ejecutar FastAPI dentro de Docker
- [ ] Configurar variables de entorno
- [ ] Crear Docker Compose
- [ ] Añadir PostgreSQL al Compose
- [ ] Probar backend + PostgreSQL completamente dockerizados

---

# Milestone 9 — CI/CD

## Pendiente

- [ ] Crear GitHub Actions
- [ ] Ejecutar tests automáticamente
- [ ] Añadir linting/formateo
- [ ] Construir imagen Docker
- [ ] Preparar deployment
- [ ] Automatizar deploy

---

# Milestone 10 — Azure

Objetivo inicial: desplegar la aplicación de forma accesible desde Internet.

## Pendiente

- [ ] Crear Resource Group
- [ ] Elegir servicio de ejecución
- [ ] Desplegar backend
- [ ] Configurar variables/secrets
- [ ] Configurar base de datos
- [ ] Configurar logs
- [ ] Comprobar aplicación desplegada
- [ ] Conectar CI/CD con Azure

---

# Fuera de scope de esta primera iteración

No implementar todavía:

- [ ] RAG
- [ ] Embeddings
- [ ] Vector Database
- [ ] Subida de documentos
- [ ] Agentes complejos
- [ ] Kubernetes
- [ ] Terraform
- [ ] Microservicios
- [ ] Autenticación
- [ ] Multiusuario
- [ ] Redis
- [ ] Fine-tuning
- [ ] MCP
- [ ] Arquitectura event-driven
- [ ] Azure AI Foundry

Estas funcionalidades se añadirán progresivamente cuando las milestones anteriores estén funcionando.

---

# Definition of Done — Backend MVP

La primera gran versión del backend estará terminada cuando:

- [ ] FastAPI funcionando
- [ ] `GET /health`
- [ ] `POST /api/chat`
- [ ] LLM local mediante Ollama
- [ ] Conversaciones persistentes
- [ ] PostgreSQL
- [ ] Streaming
- [ ] Web Search
- [ ] Tests básicos
- [ ] Docker
- [ ] CI/CD básico
- [ ] Backend desplegado en Azure

El objetivo no es implementar todo de golpe. Cada milestone debe dejar una pieza funcional antes de continuar.

---

# Siguiente acción

**La siguiente tarea inmediata es conectar el backend con el Ollama remoto.**

Antes de escribir código:

```powershell
curl http://IP_DEL_ORDENADOR_OLLAMA:11434/api/tags
```

Comprobar:

1. Que el PC de desarrollo puede acceder al servidor Ollama.
2. Qué modelos están instalados.
3. Elegir uno para desarrollo.

Después se implementará el cliente LLM y se sustituirá la respuesta simulada de `ChatService`.
