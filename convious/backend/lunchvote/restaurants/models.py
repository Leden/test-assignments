from django.db import models

from lunchvote.lib.models import UUIDModel


class Restaurant(UUIDModel):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
