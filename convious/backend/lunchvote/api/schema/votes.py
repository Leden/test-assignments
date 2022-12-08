import datetime as dt
import typing as t
from uuid import UUID

import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from lunchvote.votes.models import Vote
from lunchvote.votes.services import get_winner_history
from lunchvote.votes.services import upvote_restaurant

from .restaurants import RestaurantType


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote
        fields = ("restaurant", "user", "weight", "date")


class WinnerType(graphene.ObjectType):
    date = graphene.Date(required=True)
    restaurant = graphene.Field(RestaurantType, required=True)


class Query:
    votes = graphene.List(
        graphene.NonNull(VoteType),
        from_date=graphene.Date(required=True),
        to_date=graphene.Date(required=True),
        restaurant_uuid=graphene.UUID(),
        user_uuid=graphene.UUID(),
    )

    def resolve_votes(
        root,
        info,
        from_date: dt.date,
        to_date: dt.date,
        restaurant_uuid: UUID | None = None,
        user_uuid: UUID | None = None,
    ):
        params: dict[str, t.Tuple[dt.date, dt.date] | UUID] = {
            "date__range": (from_date, to_date)
        }
        if restaurant_uuid:
            params["restaurant__uuid"] = restaurant_uuid
        if user_uuid:
            params["user__uuid"] = user_uuid
        return Vote.objects.filter(**params).select_related("restaurant", "user")

    winners = graphene.List(
        graphene.NonNull(WinnerType),
        from_date=graphene.Date(required=True),
        to_date=graphene.Date(required=True),
    )

    def resolve_winners(root, info, from_date: dt.date, to_date: dt.date):
        return [
            WinnerType(date=date, restaurant=restaurant)
            for date, restaurant in get_winner_history(
                from_date=from_date, to_date=to_date
            ).items()
        ]


class UpvoteRestaurantInput(graphene.InputObjectType):
    restaurant_uuid = graphene.UUID(required=True)


class UpvoteRestaurant(graphene.Mutation):
    class Arguments:
        input = UpvoteRestaurantInput(required=True)

    vote = graphene.Field(VoteType)

    @login_required
    def mutate(root, info, input):
        user = info.context.user
        vote = upvote_restaurant(restaurant_uuid=input.restaurant_uuid, user=user)
        return UpvoteRestaurant(vote=vote)


class Mutation:
    upvote_restaurant = UpvoteRestaurant.Field()
