class Vector:
    """An n-dimensional vector."""

    def __init__(self, **components):
        private_components = {f"_{k}": v for k, v in components.items()}
        self.__dict__.update(private_components)

    def __getattr__(self, name):
        private_name = f"_{name}"
        try:
            return self.__dict__[private_name]
        except KeyError:
            raise AttributeError(f"{self!r} object has no attribute {name!r}")

    def __setattr__(self, name, value):
        raise AttributeError(f"Can't set attribute {name!r}")

    def __delattr__(self, name):
        raise AttributeError(f"Can't delete attribute {name!r}")

    def __repr__(self):
        return "{}({})".format(
            type(self).__name__,
            ", ".join(
                "{k}={v}".format(
                    k=k[1:],
                    v=v,
                ) for k, v in self.__dict__.items()
            )
        )