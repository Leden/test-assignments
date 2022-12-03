import itertools
import operator


class Registry:
    def __init__(self, key_spec):
        self.objects = {}
        self.default = None
        self.keyfn = self.make_keyfn(key_spec)

    def register(self, obj):
        key = self.get_key_for(obj)
        self.objects.setdefault(key, []).append(obj)
        return obj

    def register_default(self, obj):
        self.default = obj
        return obj

    def get_key_for(self, obj):
        return self.keyfn(obj)

    def make_keyfn(self, key_spec):
        if callable(key_spec):
            return key_spec
        return operator.attrgetter(key_spec)

    def get(self, key):
        return self.get_all(key)[-1]

    def get_all(self, key):
        return self.objects.get(key, [self.default])

    def values_flat(self):
        return itertools.chain.from_iterable(self.objects.values())

    def keys(self):
        return self.objects.keys()
