import factory


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "votes.Vote"

    date = factory.Faker("past_date")
    restaurant = factory.SubFactory(
        "lunchvote.restaurants.tests.factories.RestaurantFactory"
    )
    user = factory.SubFactory("lunchvote.users.tests.factories.UserFactory")
    weight = 1
