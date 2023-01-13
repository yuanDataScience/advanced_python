
class MyIterator:

    ...

    def __iter__(self):
        # All iterators are also iterables
        return self

    def __next__(self):
        if not has_more_items():
            raise StopIteration
        item = get_the_next_item()
        return item
