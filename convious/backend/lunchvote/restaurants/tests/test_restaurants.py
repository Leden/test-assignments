import pytest

from lunchvote.restaurants import services
from lunchvote.restaurants.models import Restaurant

pytestmark = pytest.mark.django_db


def test_create_restaurant(faker):
    name = faker.word()

    restaurant = services.create_restaurant(name=name)

    # Is name set correctly?
    assert restaurant.name == name

    # Is instance saved?
    assert restaurant.pk is not None

    # Can be found later by uuid or primary key?
    assert Restaurant.objects.get(uuid=restaurant.uuid) == restaurant
    assert Restaurant.objects.get(pk=restaurant.pk) == restaurant


def test_update_restaurant(faker, restaurant):
    new_name = faker.word()

    updated = services.update_restaurant(uuid=restaurant.uuid, name=new_name)

    assert updated.uuid == restaurant.uuid
    assert updated.pk == restaurant.pk
    assert updated.name == new_name

    assert Restaurant.objects.get(uuid=restaurant.uuid) == updated
    assert Restaurant.objects.get(pk=restaurant.pk) == updated


def test_delete_restaurant(faker, restaurant):
    assert Restaurant.objects.get(uuid=restaurant.uuid) == restaurant

    services.delete_restaurant(uuid=restaurant.uuid)

    with pytest.raises(Restaurant.DoesNotExist):
        Restaurant.objects.get(uuid=restaurant.uuid)
