from random import shuffle


def shuffled(iterable):
    """Randomly shuffle a copy of iterable."""
    items = list(iterable)
    shuffle(items)
    return items


def argmin_random_tie(seq, key=lambda x: x):
    """Return a minimum element of seq; break ties at random."""
    return min(shuffled(seq), key=key)


def flatten(seqs):
    return sum(seqs, [])


def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(map(bool, seq))
