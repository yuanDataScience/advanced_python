class object:

    def __getattribute__(obj, name):
        cls = type(obj)
        cls_attribute = getattr(cls, name, undefined)
        descriptor_get = getattr(type(cls_attribute), "__get__", undefined)
        if descriptor_get is not undefined:
            if (hasattr(type(cls_attribute), "__set__")
                or hasattr(type(cls_attribute), "__delete__")):
                return descriptor_get(cls_attribute, obj, cls)  # data descriptor
        if name in vars(obj):
            return vars(obj)[name]                              # instance attribute
        if descriptor_get is not undefined:
            return descriptor_get(cls_attribute, obj, cls)      # non-data descriptor
        if cls_attribute is not undefined:                       
            return cls_attribute                                # class attribute
        if hasattr(cls, "__getattr__"):
            return cls.__getattr__(obj, name)                   # __getattr__ fallback
        raise AttributeError(f"{cls.__name__} object has no attribute {name}")
