FROM bitnami/python:3.12 as builder

WORKDIR /code

ENV POETRY_VERSION=1.4.2 \
	POETRY_NO_INTERACTION=1 \
	POETRY_VIRTUALENVS_IN_PROJECT=1 \
	POETRY_VIRTUALENVS_CREATE=1 \
	POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install --only main --no-cache-dir "poetry==${POETRY_VERSION}"

COPY poetry.lock pyproject.toml ./

RUN poetry install --only main --no-root \
	&& rm -rf ${POETRY_CACHE_DIR}

FROM bitnami/python:3.12 as runner

WORKDIR /code

COPY --from=builder /code /code

COPY dash_backend /code
ENV PATH="/code/.venv/bin:$PATH"

CMD ["python","-m","backend"]
