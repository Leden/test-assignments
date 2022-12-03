#!/bin/sh

set -eux

dumpdata () {
  python manage.py dumpdata --indent=2 --natural-foreign --natural-primary "$@"
}

dump_initial_data () {
  app="$1"
  dumpdata "$@" >"lunchvote/$app/fixtures/initial_data.json"
}


python manage.py makemigrations
python manage.py migrate

dump_initial_data users auth
