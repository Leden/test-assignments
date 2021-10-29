FROM python:3.10-alpine AS builder

ARG DEVMODE

ENV APP_DIR /app
WORKDIR $APP_DIR

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.11

RUN apk add --no-cache build-base libffi-dev

RUN pip install "poetry==$POETRY_VERSION" \
    && python -m venv /venv \
    && /venv/bin/pip install wheel

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

COPY weatherapi ./weatherapi/
RUN poetry build && /venv/bin/pip install dist/*.whl


FROM python:3.10-alpine AS final

COPY --from=builder /venv /venv
COPY docker-entrypoint.sh ./

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["docker-start", "gunicorn"]
