#!/usr/bin/env bash

PROJECT="lunchvote"

[ -f /venv/bin/activate ] && . /venv/bin/activate


if [[ "$1" == "docker-start" ]]; then
  shift

  if [[ "$1" == "runserver" ]]; then
    python3 manage.py migrate
    exec python3 manage.py runserver_plus "0:$DJANGO_PORT" --nopin --nostatic
  fi

  if [[ "$1" == "gunicorn" ]]; then
    python3 manage.py migrate
    exec gunicorn "$PROJECT.wsgi:application" -w "$WORKERS_AMOUNT" --bind "0:$DJANGO_PORT" --preload
  fi

  if [[ "$1" == "celery" ]]; then
    exec celery -A "$PROJECT" worker -l info -E
  fi

  if [[ "$1" == "celerybeat" ]]; then
    rm -f celerybeat-schedule celerybeat.pid
    exec celery -A "$PROJECT" beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
  fi

  [ "$1" = "manage.py" ] && {
    shift
    python3 manage.py migrate
    exec python3 manage.py "$@"
  }
fi

exec "$@"
