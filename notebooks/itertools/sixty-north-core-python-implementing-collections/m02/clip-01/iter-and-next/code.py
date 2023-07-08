iterator = iter(iterable)

try:
    item = next(iterator)
    print(item)
except StopIteration:
    print("No more items")
