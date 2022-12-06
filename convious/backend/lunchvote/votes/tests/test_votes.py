import datetime as dt

from django.utils import timezone

import pytest

from lunchvote.votes import services
from lunchvote.votes.models import Vote

pytestmark = pytest.mark.django_db


def test_get_user_votes_per_day(faker, settings):
    settings.LUNCHVOTE_VOTES_USER_VOTES_PER_DAY = votes_per_day = faker.pyint(1, 10)
    assert votes_per_day == services.get_user_votes_per_day()


def test_get_vote_weight(user, restaurant, faker, settings):
    date = faker.date()
    settings.LUNCHVOTE_VOTES_USER_VOTES_PER_DAY = 5

    weight = services.get_vote_weight(user=user, restaurant=restaurant, date=date)
    assert weight == 1

    Vote.objects.create(user=user, restaurant=restaurant, date=date, weight=weight)

    weight = services.get_vote_weight(user=user, restaurant=restaurant, date=date)
    assert weight == 1 / 2

    Vote.objects.create(user=user, restaurant=restaurant, date=date, weight=weight)

    weight = services.get_vote_weight(user=user, restaurant=restaurant, date=date)
    assert weight == 1 / 4

    Vote.objects.create(user=user, restaurant=restaurant, date=date, weight=weight)

    weight = services.get_vote_weight(user=user, restaurant=restaurant, date=date)
    assert weight == 1 / 4

    Vote.objects.create(user=user, restaurant=restaurant, date=date, weight=weight)

    weight = services.get_vote_weight(user=user, restaurant=restaurant, date=date)
    assert weight == 1 / 4

    Vote.objects.create(user=user, restaurant=restaurant, date=date, weight=weight)


def test_create_vote(user, restaurant, faker):
    date = faker.date()

    weight = services.get_vote_weight(user=user, restaurant=restaurant, date=date)
    vote = services.create_vote(user=user, restaurant=restaurant, date=date)
    assert vote.date == date
    assert vote.user == user
    assert vote.restaurant == restaurant
    assert vote.weight == weight

    assert vote == Vote.objects.get(pk=vote.pk)
    assert vote == Vote.objects.get(uuid=vote.uuid)


def test_create_vote_exceeds_limit(user, restaurant, faker, settings):
    date = faker.date()
    settings.LUNCHVOTE_VOTES_USER_VOTES_PER_DAY = 0

    with pytest.raises(ValueError, match="exceeded the daily votes limit"):
        services.create_vote(user=user, restaurant=restaurant, date=date)


def test_upvote_restaurant(user, restaurant):
    today = timezone.now().date()

    weight = services.get_vote_weight(user=user, restaurant=restaurant, date=today)
    vote = services.upvote_restaurant(restaurant_uuid=restaurant.uuid, user=user)
    assert vote.date == today
    assert vote.user == user
    assert vote.restaurant == restaurant
    assert vote.weight == weight


def test_get_winner_history(user_factory, restaurant_factory, faker, settings):
    # 5 users have voted for 3 restaurants over 4 (consecutive) days.
    u1, u2, u3, u4, u5 = user_factory.create_batch(5)
    r1, r2, r3 = restaurant_factory.create_batch(3)
    d1 = faker.past_date()
    d2 = d1 + dt.timedelta(days=1)
    d3 = d2 + dt.timedelta(days=1)
    d4 = d3 + dt.timedelta(days=1)

    # Maximum number of votes per user is set to 4 (by a fair dice roll).
    settings.LUNCHVOTE_VOTES_USER_VOTES_PER_DAY = 4

    #  |____________Day_1___________|
    #  |       |  r1  |  r2  |  r3  |
    #  | user1 | **   | **   |      |
    #  | user2 | *    | *    | **   |
    #  | user3 | *    | **   | *    |
    #  | user4 | *    | **   | *    |
    #  | user5 | *    |      | ***  |
    #  |_total_|_5.50_|_5.50_|_5.25_|
    #  * This is a tie between r1 and r2. R1 wins by the number of voters (5 vs 4).
    services.create_vote(date=d1, user=u1, restaurant=r1)
    services.create_vote(date=d1, user=u1, restaurant=r1)
    services.create_vote(date=d1, user=u1, restaurant=r2)
    services.create_vote(date=d1, user=u1, restaurant=r2)

    services.create_vote(date=d1, user=u2, restaurant=r1)
    services.create_vote(date=d1, user=u2, restaurant=r2)
    services.create_vote(date=d1, user=u2, restaurant=r3)
    services.create_vote(date=d1, user=u2, restaurant=r3)

    services.create_vote(date=d1, user=u3, restaurant=r1)
    services.create_vote(date=d1, user=u3, restaurant=r2)
    services.create_vote(date=d1, user=u3, restaurant=r2)
    services.create_vote(date=d1, user=u3, restaurant=r3)

    services.create_vote(date=d1, user=u4, restaurant=r1)
    services.create_vote(date=d1, user=u4, restaurant=r2)
    services.create_vote(date=d1, user=u4, restaurant=r2)
    services.create_vote(date=d1, user=u4, restaurant=r3)

    services.create_vote(date=d1, user=u5, restaurant=r1)
    services.create_vote(date=d1, user=u5, restaurant=r3)
    services.create_vote(date=d1, user=u5, restaurant=r3)
    services.create_vote(date=d1, user=u5, restaurant=r3)

    #  |____________Day_2___________|
    #  |       |  r1  |  r2  |  r3  |
    #  | user1 | **** |      |      |
    #  | user2 | *    | *    | **   |
    #  | user3 | *    | ***  |      |
    #  | user4 | **   | **   |      |
    #  | user5 |      | *    | ***  |
    #  |_total_|_5.50_|_5.25_|_3.25_|
    #  * R1 wins by the total points.
    services.create_vote(date=d2, user=u1, restaurant=r1)
    services.create_vote(date=d2, user=u1, restaurant=r1)
    services.create_vote(date=d2, user=u1, restaurant=r1)
    services.create_vote(date=d2, user=u1, restaurant=r1)

    services.create_vote(date=d2, user=u2, restaurant=r1)
    services.create_vote(date=d2, user=u2, restaurant=r2)
    services.create_vote(date=d2, user=u2, restaurant=r3)
    services.create_vote(date=d2, user=u2, restaurant=r3)

    services.create_vote(date=d2, user=u3, restaurant=r1)
    services.create_vote(date=d2, user=u3, restaurant=r2)
    services.create_vote(date=d2, user=u3, restaurant=r2)
    services.create_vote(date=d2, user=u3, restaurant=r2)

    services.create_vote(date=d2, user=u4, restaurant=r1)
    services.create_vote(date=d2, user=u4, restaurant=r1)
    services.create_vote(date=d2, user=u4, restaurant=r2)
    services.create_vote(date=d2, user=u4, restaurant=r2)

    services.create_vote(date=d2, user=u5, restaurant=r2)
    services.create_vote(date=d2, user=u5, restaurant=r3)
    services.create_vote(date=d2, user=u5, restaurant=r3)
    services.create_vote(date=d2, user=u5, restaurant=r3)

    #  |____________Day_3___________|
    #  |       |  r1  |  r2  |  r3  |
    #  | user1 |      |      | *    |
    #  | user2 | *    | *    | **   |
    #  | user3 | *    | ***  |      |
    #  | user4 | **   | **   |      |
    #  | user5 |      | *    | ***  |
    #  |_total_|_3.50_|_5.25_|_4.25_|
    #  * User1 got sick and didn't use all of the available votes that day.
    #    Everyone else voted as before.
    #  * R2 wins by weight sum.
    services.create_vote(date=d3, user=u1, restaurant=r3)

    services.create_vote(date=d3, user=u2, restaurant=r1)
    services.create_vote(date=d3, user=u2, restaurant=r2)
    services.create_vote(date=d3, user=u2, restaurant=r3)
    services.create_vote(date=d3, user=u2, restaurant=r3)

    services.create_vote(date=d3, user=u3, restaurant=r1)
    services.create_vote(date=d3, user=u3, restaurant=r2)
    services.create_vote(date=d3, user=u3, restaurant=r2)
    services.create_vote(date=d3, user=u3, restaurant=r2)

    services.create_vote(date=d3, user=u4, restaurant=r1)
    services.create_vote(date=d3, user=u4, restaurant=r1)
    services.create_vote(date=d3, user=u4, restaurant=r2)
    services.create_vote(date=d3, user=u4, restaurant=r2)

    services.create_vote(date=d3, user=u5, restaurant=r2)
    services.create_vote(date=d3, user=u5, restaurant=r3)
    services.create_vote(date=d3, user=u5, restaurant=r3)
    services.create_vote(date=d3, user=u5, restaurant=r3)

    #  |____________Day_4___________|
    #  |       |  r1  |  r2  |  r3  |
    #  | user1 |      |      |      |
    #  | user2 |      |      |      |
    #  | user3 |      |      |      |
    #  | user4 |      |      |      |
    #  | user5 |      |      |      |
    #  |_total_|_0.00_|_0.00_|_0.00_|
    #  * Day 4 was a holiday: nobody voted, and there is no winner.

    # Check who won on which day
    # N.b. Day 4 is not returned as there is no winner on that day.
    assert services.get_winner_history(from_date=d1, to_date=d4) == {
        d1: r1,
        d2: r1,
        d3: r2,
    }
