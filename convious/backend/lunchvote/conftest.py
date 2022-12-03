import importlib
import inspect

from django.apps import apps

import factory
import pytest_factoryboy

# Register factories from all apps within lunchvote

for app_config in apps.get_app_configs():
    if not app_config.name.startswith("lunchvote"):
        continue

    factories_module = importlib.import_module(".tests.factories", app_config.name)

    factory_classes = [
        klass
        for (name, klass) in inspect.getmembers(factories_module, inspect.isclass)
        if name.endswith("Factory") and issubclass(klass, factory.Factory)
    ]

    models_with_factories = {klass._meta.model for klass in factory_classes}
    if missing := set(app_config.get_models()) - models_with_factories:
        raise ValueError(f"Factory for model(s) {missing} is not defined.")

    for klass in factory_classes:
        pytest_factoryboy.register(klass)
