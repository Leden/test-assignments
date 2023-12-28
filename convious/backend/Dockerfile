FROM python:3.11.0 AS base

ENV APP_DIR /app

WORKDIR $APP_DIR/


FROM base AS builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.7

COPY pyproject.toml poetry.lock ./
RUN python -m venv /venv && \
    pip install "poetry==$POETRY_VERSION" && \
    poetry export --dev -f requirements.txt --without-hashes | /venv/bin/pip install -r /dev/stdin


FROM builder AS django

RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list && \
    apt-get update && \
    apt-get install -y postgresql-client-12

COPY --from=builder /venv /venv

COPY docker-entrypoint.sh ./

COPY . .
RUN  . /venv/bin/activate \
  && ./manage.py collectstatic -v3 --noinput

RUN echo ". /venv/bin/activate" >> "$HOME/.bashrc"

ENV DJANGO_PORT 8000

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]

# CMD options:
#
# CMD ["docker-start", "runserver"]
# CMD ["docker-start", "celery"]
# CMD ["docker-start", "celerybeat"]

CMD ["docker-start", "runserver"]
