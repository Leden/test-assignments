import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.User"

    is_superuser = False
    is_staff = False
    is_active = True

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    email = factory.Faker("email")
    username = factory.SelfAttribute("email")
    password = factory.Faker("password")
