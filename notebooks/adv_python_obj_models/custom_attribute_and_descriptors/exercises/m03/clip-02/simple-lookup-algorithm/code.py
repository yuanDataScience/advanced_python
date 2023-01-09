class object:
    """
    This code is illustrative. The real object class and its methods are implemented in C.
    """

    def __getattribute__(obj, name):
        cls = type(obj)
        if name in vars(obj):
            return vars(obj)[name]
        if hasattr(cls, name):
            return getattr(cls, name)
        if hasattr(cls, "__getattr__"):
            return cls.__getattr__(obj, name)
        raise AttributeError(f"{cls.__name__} object has no attribute {name}")