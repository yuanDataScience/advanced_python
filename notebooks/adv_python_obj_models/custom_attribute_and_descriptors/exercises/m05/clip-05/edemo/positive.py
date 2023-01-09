from weakref import WeakKeyDictionary


class Positive:
    """A data-descriptor for positive numeric values."""

    def __init__(self):
        self._instance_data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self._instance_data[instance]

    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError(f"Value {value} is not positive")
        self._instance_data[instance] = value

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute")
