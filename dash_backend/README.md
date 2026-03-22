
### Quickstart
To run just the backend API, run the following:

```
poetry install
poetry run python -m dash_backend --reload
```
There must be an active database reachable through the DB url parameters set in `dash_database.config`, the docker-compose in the repository root directory launches one. It can be worth running that docker-compose even when running the backend separately for development.

### Database migrations (Alembic)

From `dash_backend` (with the same `.env` / `POSTGRES_*` settings as the app).

**Empty database (no tables yet):** run migrations so Alembic actually creates the schema.

```bash
poetry run alembic upgrade head
```

New revisions: `poetry run alembic revision --autogenerate -m "description"` then review the generated file before applying.