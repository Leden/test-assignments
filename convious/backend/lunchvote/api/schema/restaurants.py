import graphene
from graphene_django import DjangoObjectType

from lunchvote.restaurants.models import Restaurant
from lunchvote.restaurants.services import create_restaurant
from lunchvote.restaurants.services import delete_restaurant
from lunchvote.restaurants.services import update_restaurant


class RestaurantType(DjangoObjectType):
    class Meta:
        model = Restaurant
        fields = ("uuid", "name")


class Query:
    restaurants = graphene.List(graphene.NonNull(RestaurantType))

    def resolve_restaurants(root, info):
        return Restaurant.objects.all()

    restaurant = graphene.Field(RestaurantType, uuid=graphene.UUID(required=True))

    def resolve_restaurant(root, info, uuid):
        return Restaurant.objects.get(uuid=uuid)


class CreateRestaurantInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class CreateRestaurant(graphene.Mutation):
    class Arguments:
        input = CreateRestaurantInput(required=True)

    restaurant = graphene.Field(graphene.NonNull(RestaurantType))

    def mutate(root, info, input):
        restaurant = create_restaurant(name=input.name)
        return CreateRestaurant(restaurant=restaurant)


class UpdateRestaurantInput(graphene.InputObjectType):
    uuid = graphene.UUID(required=True)
    name = graphene.String(required=True)


class UpdateRestaurant(graphene.Mutation):
    class Arguments:
        input = UpdateRestaurantInput(required=True)

    restaurant = graphene.Field(graphene.NonNull(RestaurantType))

    def mutate(root, info, input):
        restaurant = update_restaurant(uuid=input.uuid, name=input.name)
        return UpdateRestaurant(restaurant=restaurant)


class DeleteRestaurantInput(graphene.InputObjectType):
    uuid = graphene.UUID(required=True)


class DeleteRestaurant(graphene.Mutation):
    class Arguments:
        input = DeleteRestaurantInput(required=True)

    restaurant = graphene.Field(graphene.NonNull(RestaurantType))

    def mutate(root, info, input):
        restaurant = delete_restaurant(uuid=input.uuid)
        return DeleteRestaurant(restaurant=restaurant)


class Mutation:
    create_restaurant = CreateRestaurant.Field()
    update_restaurant = UpdateRestaurant.Field()
    delete_restaurant = DeleteRestaurant.Field()
