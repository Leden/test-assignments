#!/bin/sh

set -eux

[ -z "$DJANGO_DEBUG" ] && {
    echo "This command only works in dev environment"
    exit 1
}

filename=$(find . -name '*.sql' -type f | tail -n 1)

python manage.py reset_db --noinput -c
python manage.py dbshell <"$filename"
python manage.py migrate
