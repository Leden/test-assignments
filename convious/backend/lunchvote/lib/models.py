import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

import reversion


def generic_model_str(model, only=None):
    field_values = {
        f.name: getattr(model, f.name, None)
        for f in model._meta.get_fields()
        if not getattr(f, "field", None) and (only is None or f.name in only)
    }
    pairs = " ".join(f"{k}={v!r}" for k, v in field_values.items())
    return pairs


class TimestampedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)


class UUIDModel(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True)


class VersionsMixin:
    @property
    def versions(self):
        return reversion.models.Version.objects.get_for_object(self)
