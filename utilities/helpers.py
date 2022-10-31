
from threading import Thread


def select(_iter, func):
    results = []
    for item in _iter:
        results.append(func(item))
    return results
