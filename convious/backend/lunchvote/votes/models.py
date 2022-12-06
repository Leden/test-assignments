from django.db import models

from lunchvote.lib.models import UUIDModel


class Vote(UUIDModel):
    date = models.DateField()
    restaurant = models.ForeignKey(
        "restaurants.Restaurant", on_delete=models.CASCADE, related_name="votes"
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    weight = models.DecimalField(decimal_places=2, max_digits=5)
