class object:
    """
    This code is illustrative. The real object class and its methods are implemented in C.
    """

    def __getattribute__(obj, name):
        cls = type(obj)
        if hasattr(cls, "__slots__"):
            if name in cls.__slots__:
                index = cls.__slots__.index(name)
                return obj.slot_array[index]
        if name in vars(obj):
            return vars(obj)[name]
        if hasattr(cls, name):
            return getattr(cls, name)
        if hasattr(cls, "__getattr__"):
            return cls.__getattr__(obj, name)
        raise AttributeError(f"{cls.__name__} object has no attribute {name}")