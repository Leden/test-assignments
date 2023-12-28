import factory


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "restaurants.Restaurant"

    name = factory.Faker("word")
