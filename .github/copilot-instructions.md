<!-- Copilot instructions for DadsDashApp -->

# DadsDashApp — Copilot Instructions

This file contains concise, repository-specific guidance for AI coding agents working on DadsDashApp.

- **Big picture**: this repo has two main pieces:
  - Backend: a FastAPI service in `dash_backend` (source under `dash_backend/src/dash_backend`). It handles Strava auth, fetches activities via `stravalib`, persists data in `dash_database` and exposes JSON endpoints (see `dash_backend/src/dash_backend/api/api.py`).
  - Frontend: a Next.js React app in `dash_frontend` (ports: development `3000`). The frontend calls backend endpoints and expects token-based query parameters (see `dash_frontend/src/api/api_call.ts`).

- **How to run locally (developer shortcuts)**
  - Full stack (recommended dev): `docker-compose up` from repo root. Docker-compose starts Postgres + pgAdmin + backend (frontend is commented out).
  - Backend only (iterative development):
    ```bash
    cd dash_backend
    poetry install
    poetry run python -m dash_backend --reload
    ```
    The backend reads environment values via `dash_backend/src/dash_backend/config.py` (env prefix `API_`) and `dash_backend/src/dash_database/config.py` (env prefix `POSTGRES_`). Use `example.env` as a template for `.env`.
  - Frontend: `cd dash_frontend && npm install && npm run dev` (opens at `http://localhost:3000`). The frontend expects the backend at port `8000` when running via docker-compose.

- **Key files to inspect for behavior & patterns**
  - Backend entrypoint: `dash_backend/src/dash_backend/__main__.py` (starts uvicorn using `ApiConfig`)
  - API routes and token usage: `dash_backend/src/dash_backend/api/api.py` — note many routes accept `token` as a query parameter (not as a header).
  - DB layer: `dash_backend/src/dash_database/*` — `session.py`, `crud.py`, `models.py` and `config.py` show how sessions and schemas are used.
  - Strava integration: `dash_backend/src/dash_backend/strava/strava_client.py` and `strava_utils.py`.

- **Project conventions & patterns**
  - Source layout uses a `src/` top-level package layout (packages declared in `pyproject.toml`). Keep imports rooted at package names (e.g., `from dash_backend...`).
  - Environment config: backend uses `pydantic-settings.BaseSettings` with explicit `env_prefix` values. Do not assume `.env` defaults; consult `ApiConfig` and `DbConfig` for expected variable names and prefixes.
  - Database sessions: functions use a `get_db()` dependency that yields `SessionLocal()` (close the session after use). Prefer adding new DB interactions through `dash_database/crud.py`.
  - Token handling: current design passes Strava token as a query parameter to endpoints (e.g., `/hero-stats?token=...`). When modifying auth, update all callers (frontend and tests).

- **Build/test/debug tips**
  - No automated tests present; run the backend with `--reload` and use Postman or browser to hit endpoints.
  - To inspect DB during dev, use `pgadmin` started by `docker-compose` (port `15433`) or connect psql to `localhost:5432`.

- **When making changes**
  - Small backend changes: run locally with poetry and verify endpoints. If changing DB schema, prefer migration notes (no migrations present in repo).
  - Frontend changes: run `npm run dev` and check `console` + network panel for token/query param usage.

- **Examples to reference when coding**
  - Exchange access code for token: `GET /login?access_code=...` implemented in `dash_backend/src/dash_backend/api/api.py` (calls `athlete_login`).
  - Read/write athlete and activities via `dash_database/crud.py` (used throughout `api.py`).

- **Limitations & safe-guards for AI agents**
  - Avoid changing auth flow (token-as-query) unless both backend and frontend are updated together.
  - Do not assume migrations or test harnesses exist; include manual verification steps when recommending DB schema changes.

If anything here is unclear or you want more detail on a section (examples, run scripts, or conventions), tell me which part to expand or correct.
