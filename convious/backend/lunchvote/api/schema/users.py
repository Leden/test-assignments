import graphene
from graphene_django import DjangoObjectType

from lunchvote.users.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("uuid", "first_name", "last_name")


class CurrentUserType(UserType):
    class Meta:
        skip_registry = True
        model = User
        fields = (*UserType._meta.fields, "email")


class Query:
    me = graphene.Field(CurrentUserType)

    def resolve_me(root, info):
        user = info.context.user
        return user if user.is_authenticated else None
