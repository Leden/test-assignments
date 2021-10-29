#!/usr/bin/env sh

[ -f /venv/bin/activate ] && . /venv/bin/activate

if [[ "$1" == "docker-start" ]]; then
  shift

  if [[ "$1" == "gunicorn" ]]; then
    exec gunicorn weatherapi.app:app \
        -w "$WORKERS_AMOUNT" \
        --bind "0:$HTTP_PORT" \
        --preload \
        --worker-class aiohttp.GunicornWebWorker \
        --access-logfile -
  fi
fi

exec "$@"
