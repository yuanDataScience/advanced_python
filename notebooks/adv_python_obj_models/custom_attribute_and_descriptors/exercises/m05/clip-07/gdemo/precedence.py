class DataDescriptor:

    def __get__(self, instance, owner):
        print(f"{type(self).__name__}.__get__({self!r}, {instance!r}, {owner!r}")

    def __set__(self, instance, value):
        print(f"{type(self).__name__}.__set__({self!r}, {instance!r}, {owner!r}")


class NonDataDescriptor:

    def __get__(self, instance, owner):
        print(f"{type(self).__name__}.__get__({self!r}, {instance!r}, {owner!r}")


class Owner:

      a = DataDescriptor()
      b = NonDataDescriptor()

