iterable_list = [2, 4, 6, 8, 10]
iterable_tuple = ("orange", "apple", "banana")
iterable_dict = dict(a="alpha", b="bravo", c="charlie")

def iterable_oceans():
    yield "Arctic"
    yield "Atlantic"
    yield "Indian"
    yield "Pacific"
    yield "Southern"

iterable_squares = (x*x for x in range(10))
