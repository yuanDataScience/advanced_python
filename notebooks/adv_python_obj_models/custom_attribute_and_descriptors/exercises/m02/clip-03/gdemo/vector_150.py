class Vector:
    """An n-dimensional vector."""

    def __init__(self, **components):
        private_components = {f"_{k}": v for k, v in components.items()}
        self.__dict__.update(private_components)

    def __getattr__(self, name):
        private_name = f"{name=}"
        print(private_name)

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
