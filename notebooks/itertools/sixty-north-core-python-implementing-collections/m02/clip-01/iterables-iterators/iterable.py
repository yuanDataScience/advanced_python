class MyIterable:

    ...

    def __iter__(self):
        # Must return a new iterator
        # for this iterable
        iterator = MyIterator(self)
        return iterator

iterator = iter(iterable)

item = next(iterator)
