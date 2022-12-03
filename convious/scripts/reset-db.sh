#!/bin/sh

set -eux

[ -z "$DJANGO_DEBUG" ] && {
    echo "This command only works in dev environment"
    exit 1
}

APPS="users"

python manage.py reset_db --noinput -c
python manage.py migrate

printf '%s' "$APPS" \
  | xargs -I {} python manage.py loaddata initial_data --app {}

python manage.py createinitialrevisions
