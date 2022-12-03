import pytest

pytestmark = pytest.mark.django_db


def test_user_email(user):
    assert "@" in user.email


def test_user_username_eq_email(user):
    assert user.username == user.email
