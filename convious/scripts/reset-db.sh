#!/bin/sh

set -eux

[ -z "$DJANGO_DEBUG" ] && {
    echo "This command only works in dev environment"
    exit 1
}

APPS="users restaurants"


python manage.py reset_db --noinput -c
python manage.py migrate

for app in $APPS
do
  python manage.py loaddata initial_data --app "$app"
done

python manage.py createinitialrevisions
