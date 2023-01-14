def _is_perfect_length(sequence):
    """True if sequence has length 2ⁿ - 1, otherwise False.
    """
    n = len(sequence)
    return ((n + 1) & n == 0) and (n != 0)

def _left_child(index):
    return 2 * index + 1


def _right_child(index):
    return 2 * index + 2