import datetime as dt
import typing as t
from decimal import Decimal as D
from uuid import UUID

from django.conf import settings
from django.db.models import Count
from django.db.models import OuterRef
from django.db.models import Subquery
from django.db.models import Sum
from django.utils import timezone

from lunchvote.restaurants.models import Restaurant
from lunchvote.users.models import User

from .models import Vote


def get_user_votes_per_day() -> int:
    """
    Returns max number of votes per day each user has.
    """
    return settings.LUNCHVOTE_VOTES_USER_VOTES_PER_DAY


def get_vote_weight(*, user: User, restaurant: Restaurant, date: dt.date) -> D:
    """
    Returns the effective weight that will be applied to the NEXT vote of the given
    User on the given Restaurant on the given date.
    """
    prev_votes_count = Vote.objects.filter(
        user=user, restaurant=restaurant, date=date
    ).count()

    if prev_votes_count == 0:
        return D("1")
    elif prev_votes_count == 1:
        return D(".5")

    return D(".25")


def create_vote(*, user: User, restaurant: Restaurant, date: dt.date) -> Vote:
    """
    Returns the freshly created Vote object for the given User, Restaurant and date,
    with the correct weight.
    See also: `upvote_restaurant`.
    """
    # Validate user has not exceeded the daily limit of votes
    limit = get_user_votes_per_day()
    if Vote.objects.filter(user=user, date=date).count() >= limit:
        raise ValueError(f"User has exceeded the daily votes limit: {limit}")

    weight = get_vote_weight(user=user, restaurant=restaurant, date=date)

    vote = Vote.objects.create(
        date=date, restaurant=restaurant, user=user, weight=weight
    )

    return vote


def upvote_restaurant(*, restaurant_uuid: UUID, user: User) -> Vote:
    """
    Records and returns a new Vote for the given User and Restaurant and current date.
    Current date is determined by the server time.
    """
    today = timezone.now().date()
    restaurant = Restaurant.objects.get(uuid=restaurant_uuid)
    return create_vote(user=user, restaurant=restaurant, date=today)


def get_winner_history(
    *, from_date: dt.date, to_date: dt.date
) -> dict[dt.date, Restaurant]:
    """
    Calculates history of winners for a given interval of dates.

    Returns a mapping of dates in the specified interval as keys, and Restaurant
    instances as values.

    Only existing winners are returned: if vote did not happen on a particular date
    within the given interval, that date will not be present in the result.
    """
    # Begin with a set of dates within the interval.
    # For each date, find a restaurant_id such that
    # the sum of votes for that restaurant is the biggest.
    # Use number of unique voters as a tie-breaker (secondary sort field)
    winners_by_date = dict(
        Vote.objects.filter(date__range=(from_date, to_date))
        .distinct("date")
        .values("date")
        .annotate(
            winner_id=Subquery(
                Vote.objects.filter(date=OuterRef("date"))
                .values("restaurant_id")
                .annotate(
                    weight_sum=Sum("weight"),
                    voters_count=Count("user_id", distinct=True),
                )
                .order_by("-weight_sum", "-voters_count")
                .values("restaurant_id")[:1]
            )
        )
        .values_list("date", "winner_id")
        .order_by("date")
    )

    # Swap restaurant IDs (int) for Restaurant model instances for the final result.
    restaurants_by_id = Restaurant.objects.in_bulk(winners_by_date.values())
    return {d: restaurants_by_id[id] for d, id in winners_by_date.items()}


def get_restaurant_today_votes(*, restaurant: Restaurant) -> t.Iterable[Vote]:
    today = timezone.now().date()
    return restaurant.votes.filter(date=today)
