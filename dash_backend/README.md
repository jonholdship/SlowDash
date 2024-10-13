
### Quickstart
To run just the backend API, run the following:

```
poetry install
poetry run python -m dash_backend --reload
```
There must be an active database reachable through the DB url parameters set in `dash_database.config`, the docker-compose in the repository root directory launches one. It can be worth running that docker-compose even when running the backend separately for development.