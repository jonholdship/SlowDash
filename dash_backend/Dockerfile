FROM python:3.12-slim as builder

WORKDIR /code

ENV POETRY_VERSION=1.4.2 \
	POETRY_NO_INTERACTION=1 \
	POETRY_VIRTUALENVS_IN_PROJECT=1 \
	POETRY_VIRTUALENVS_CREATE=1 \
	POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install --only main --no-cache-dir "poetry==${POETRY_VERSION}"

COPY poetry.lock pyproject.toml README.md ./
COPY src /code/src

RUN poetry install --only main \
	&& rm -rf ${POETRY_CACHE_DIR}

FROM python:3.12-slim as runner

WORKDIR /code

COPY --from=builder /code /code

COPY src /code
ENV PATH="/code/.venv/bin:$PATH"

CMD ["python","-m","dash_backend"]