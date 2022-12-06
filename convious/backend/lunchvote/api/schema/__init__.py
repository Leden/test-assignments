import graphene

from . import restaurants
from . import users
from . import votes


class Query(restaurants.Query, users.Query, votes.Query, graphene.ObjectType):
    pass


class Mutation(restaurants.Mutation, votes.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
