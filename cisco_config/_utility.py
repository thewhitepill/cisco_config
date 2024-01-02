__all__ = (
    "find",
)


def find(predicate, iterable, *, default=None):
    for item in iterable:
        if predicate(item):
            return item

    return default
