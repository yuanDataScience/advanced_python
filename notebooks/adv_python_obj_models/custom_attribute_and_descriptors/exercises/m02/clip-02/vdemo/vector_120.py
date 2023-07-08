class Vector:
    """An n-dimensional vector."""

    def __init__(self, **components):
        self.__dict__.update(components)

    def __repr__(self):
        return "{}({})".format(
            type(self).__name__,
            ", ".join(
                "{k}={v}".format(
                    k=k,
                    v=v,
                ) for k, v in self.__dict__.items()
            )
        )
