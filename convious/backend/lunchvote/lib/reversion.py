import functools

from django.db import models

import reversion


def create_revision(*_args, **_kwargs):
    def decorator(fn):
        @functools.wraps(fn)
        @reversion.create_revision(*_args, **_kwargs)
        def _wrapper(*args, **kwargs):
            reversion.set_comment(_format_call(fn, args, kwargs))
            _add_to_revision(*args, *kwargs.values())
            return fn(*args, **kwargs)

        return _wrapper

    return decorator


def _add_to_revision(*objects):
    for obj in objects:
        if isinstance(obj, models.Model) and reversion.is_registered(obj):
            reversion.add_to_revision(obj)


def _format_call(fn, args, kwargs):
    args_str = ", ".join(
        [repr(a) for a in args] + [f"{k}={repr(v)}" for k, v in kwargs.items()]
    )
    return f"{fn.__name__}({args_str})"
