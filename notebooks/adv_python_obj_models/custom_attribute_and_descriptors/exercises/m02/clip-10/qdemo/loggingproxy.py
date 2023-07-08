class LoggingProxy:
    """Intercept and log all attribute access to an object."""

    def __init__(self, target):
        super().__setattr__("target", target)

    def __getattribute__(self, name):
        target = super().__getattribute__("target")
        try:
            value = getattr(target, name)
        except AttributeError as e:
            raise AttributeError(
                "{} could not forward request {} to {}".format(
                    super().__getattribute__("__class__").__name__,
                    name,
                    target
                )
            ) from e
        print(f"Retrieved attribute {name!r} = {value!r} from {target!r}")
        return value

