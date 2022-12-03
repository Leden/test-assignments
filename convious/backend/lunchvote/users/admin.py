import django.contrib.auth.forms
from django.contrib import admin
from django.contrib import auth

from .models import User


class UserCreationForm(django.contrib.auth.forms.UserCreationForm):
    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        fields = ("username", "email")


@admin.register(User)
class UserAdmin(auth.admin.UserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
