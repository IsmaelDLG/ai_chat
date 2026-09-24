## Run with Docker Compose

The Compose setup starts three services:

- `db`: PostgreSQL with a persistent named volume
- `backend`: FastAPI on `http://localhost:8000`
- `frontend`: Vite development server on `http://localhost:5173`

Start the project from the repository root using the existing backend environment file:

```powershell
docker compose --env-file backend/.env up --build
```

The `--env-file` option supplies Compose interpolation values for both PostgreSQL and the backend. The backend service also loads `backend/.env` directly. Keep this file private; it is ignored by Git.

The backend waits for PostgreSQL to become healthy, runs `alembic upgrade head`, and then starts Uvicorn. The API documentation is available at `http://localhost:8000/docs`, and the health endpoint is `http://localhost:8000/health`.

Ollama is expected to run outside Compose on the configured LAN host. Docker Desktop must be able to reach that address from the backend container.

Stop the services with:

```powershell
docker compose down
```

Add `-v` to remove the PostgreSQL data volume as well.
