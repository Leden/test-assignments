import os

from celery import Celery

# recommended setup for celery with Django
# https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html

# set the default Django settings module for the 'celery' program.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "lunchvote.settings",
)

app = Celery("lunchvote")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
