from uuid import UUID

from .models import Restaurant


def create_restaurant(*, name: str) -> Restaurant:
    restaurant = Restaurant.objects.create(name=name)
    return restaurant


def update_restaurant(*, uuid: UUID, name: str) -> Restaurant:
    restaurant = Restaurant.objects.get(uuid=uuid)
    restaurant.name = name
    restaurant.save()
    return restaurant


def delete_restaurant(*, uuid: UUID) -> None:
    restaurant = Restaurant.objects.get(uuid=uuid)
    restaurant.delete()
    return restaurant
