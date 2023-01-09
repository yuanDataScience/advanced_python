from weakref import WeakKeyDictionary


class Positive:
    """A data-descriptor for positive numeric values."""

    def __init__(self):
        self._instance_data = WeakKeyDictionary()

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._instance_data[instance]

    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError(f"{self._name} {value} is not positive")
        self._instance_data[instance] = value

    def __delete__(self, instance):
        raise AttributeError(f"Cannot delete attribute {self._name}")
