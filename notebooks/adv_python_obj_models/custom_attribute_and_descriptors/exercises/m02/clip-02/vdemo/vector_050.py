class Vector:
    """A two-dimensional vector."""

    def __init__(self, **components):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{type(self).__name__}({self.x}, {self.y})"