# AI Chat

## Introduction

AI Chat is a full-stack conversational application built as a monorepo with a Python backend and a TypeScript frontend. The project is designed to evolve from a simple MVP into a more complete AI application with persistent conversations, local LLM integration, streaming responses, Docker support, and future cloud-ready capabilities.

The backend is built with FastAPI and PostgreSQL, and it is designed to work with a local or remote LLM service such as Ollama. The frontend is a lightweight React + Vite interface for interacting with the chat API.

This repository is structured to keep the API, data layer, and UI separated while staying easy to run locally during early development.

---

## Repository Structure

```text
ai-chat/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── alembic/
│   ├── .env
│   ├── Dockerfile
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docs/
│   └── backend-roadmap.md
├── compose.yaml
├── README.md
└── .gitignore
```

### Main components

- `backend/`: FastAPI backend, business logic, repositories, database models, and tests.
- `frontend/`: Vite React application for the user interface.
- `docs/`: design notes, roadmap, and reference documents.
- `compose.yaml`: local development orchestration for PostgreSQL, backend, and frontend.

For the detailed project roadmap and Milestones, see [docs/backend-roadmap.md](docs/backend-roadmap.md).

---

## Installation Instructions

### Prerequisites

Before starting the project, make sure you have:

- Docker and Docker Compose installed
- Git available on your machine
- Access to a PostgreSQL instance and a compatible LLM backend such as Ollama
- A local environment file for the backend with the required variables

### 1. Clone the repository

```bash
git clone <repository-url>
cd ai_chat
```

### 2. Configure environment variables

Create a `backend/.env` file with the required values for the application and database. A typical example is:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=ai_chat
LLM_BASE_URL=http://host.docker.internal:11434/v1
LLM_API_KEY=not-needed
LLM_MODEL=llama3
```

The exact values depend on your local environment and the LLM endpoint you are connecting to.

### 3. Run the project with Docker Compose

From the repository root:

```powershell
docker compose --env-file backend/.env up --build
```

This starts:

- `db`: PostgreSQL on port `5432`
- `backend`: FastAPI on `http://localhost:8000`
- `frontend`: Vite app on `http://localhost:5173`

The backend waits for PostgreSQL to become healthy and then runs migrations before starting the API.

### 4. Stop the application

```powershell
docker compose down
```

To remove the PostgreSQL data volume as well:

```powershell
docker compose down -v
```

---

## Usage Guide

### Backend API

Once the backend is running, you can access the interactive API docs here:

- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

The application exposes conversation endpoints in the backend service and can be used to:

- create a new conversation
- retrieve existing conversations
- send a user message
- receive an AI response
- persist chat history in PostgreSQL

### Frontend

Open the frontend in the browser:

- `http://localhost:5173`

From there, the UI lets you start conversations, send prompts, and read responses from the backend in a simple chat interface.

### Local LLM integration

The backend is designed to connect to an LLM service such as Ollama running on a LAN host or another reachable machine. The URL and model are configured through environment variables in `backend/.env`.

---

## Appendix: Roadmap

The project follows a staged roadmap that starts with a basic backend and progressively adds more advanced AI and cloud capabilities.

The roadmap includes milestones for:

- FastAPI and health checks
- conversation and message persistence
- PostgreSQL and Alembic migrations
- local LLM integration via Ollama
- streaming responses
- frontend basics
- Docker Compose setup
- future web search, CI/CD, and Azure deployment work

The full roadmap is documented in [docs/roadmap.md](docs/roadmap.md).

---

> The repository is intentionally organized as a monorepo so the backend and frontend can evolve together while sharing the same project lifecycle.
