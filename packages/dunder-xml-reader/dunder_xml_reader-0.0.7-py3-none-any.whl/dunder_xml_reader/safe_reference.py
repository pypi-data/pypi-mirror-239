"""A None-guarding safe referencer"""
import sys


class SafeReference:

    def __init__(self, object, default, wrap_methods=True):
        self.object = object
        self.default = default
        self.wrap_methods = wrap_methods

    def __getattr__(self, item):
        # noinspection PyBroadException
        try:
            return SafeReference(getattr(self.object, item), self.default, self.wrap_methods)
        except:
            if self.object is not self.default:
                print(f"SafeReference: Dereference fault: {self.object.__class__.__name__}.{item}", file=sys.stderr)
            return SafeReference(self.default, self.default, self.wrap_methods)

    class Iterator:
        def __init__(self, obj):
            self.obj = obj
            self.max_index = len(obj)
            self.current_index = 0

        def __next__(self):
            if self.current_index < self.max_index:
                self.current_index += 1
                return self.obj[self.current_index-1]
            raise StopIteration

    def __iter__(self):
        return SafeReference.Iterator(self)

    def __getitem__(self, item):
        # noinspection PyBroadException
        try:
            return SafeReference(self.object.__getitem__(item), self.default, self.wrap_methods)
        except:
            return SafeReference(self.default, self.default, self.wrap_methods)

    def __len__(self):
        return len(self.object)

    def __repr__(self):
        return str(self.object)

    def __bool__(self):
        return bool(self.object)

    def __eq__(self, other):
        return other == self.object

    def __call__(self, *args, **kwargs):
        if self.wrap_methods:
            if callable(self.object):
                return SafeReference(self.object(*args, *kwargs), self.default, self.wrap_methods)
            else:
                return SafeReference(self.default, self.default, self.wrap_methods)
        else:
            return self.object(*args, *kwargs)
