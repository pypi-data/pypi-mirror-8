# coding: utf-8

from __future__ import unicode_literals, division, print_function

"""
This module provides utilities for basic math operations.
"""

import itertools
import collections
import numpy as np
from six.moves import zip


def sort_dict(d, key=None, reverse=False):
    """
    Sorts a dict by value.

    Args:
        d: Input dictionary
        key: Function which takes an tuple (key, object) and returns a value to
            compare and sort by. By default, the function compares the values
            of the dict i.e. key = lambda t : t[1]
        reverse: Allows to reverse sort order.

    Returns:
        OrderedDict object whose keys are ordered according to their value.
    """
    kv_items = [kv for kv in d.items()]

    # Sort kv_items according to key.
    if key is None:
        kv_items.sort(key=lambda t: t[1], reverse=reverse)
    else:
        kv_items.sort(key=key, reverse=reverse)

    # Build ordered dict.
    return collections.OrderedDict(kv_items)


def min_max_indexes(seq):
    """
    Uses enumerate, max, and min to return the indices of the values
    in a list with the maximum and minimum value:
    """
    minimum = min(enumerate(seq), key=lambda s: s[1])
    maximum = max(enumerate(seq), key=lambda s: s[1])
    return minimum[0], maximum[0]


def strictly_increasing(values):
    """True if values are stricly increasing."""
    return all(x < y for x, y in zip(values, values[1:]))


def strictly_decreasing(values):
    """True if values are stricly decreasing."""
    return all(x > y for x, y in zip(values, values[1:]))


def non_increasing(values):
    """True if values are not increasing."""
    return all(x >= y for x, y in zip(values, values[1:]))


def non_decreasing(values):
    """True if values are not decreasing."""
    return all(x <= y for x, y in zip(values, values[1:]))


def monotonic(values, mode="<", atol=1.e-8):
    """
    Returns False if values are not monotonic (decreasing|increasing).
    mode is "<" for a decreasing sequence, ">" for an increasing sequence.
    Two numbers are considered equal if they differ less that atol.

    .. warning:
        Not very efficient for large data sets.

    >>> values = [1.2, 1.3, 1.4]
    >>> monotonic(values, mode="<")
    False
    >>> monotonic(values, mode=">")
    True
    """
    if len(values) == 1:
        return True

    if mode == ">":
        for i in range(len(values)-1):
            v, vp = values[i], values[i+1]
            if abs(vp - v) > atol and vp <= v:
                return False

    elif mode == "<":
        for i in range(len(values)-1):
            v, vp = values[i], values[i+1]
            if abs(vp - v) > atol and vp >= v:
                return False

    else:
        raise ValueError("Wrong mode %s" % str(mode))

    return True


if __name__ == "__main__":
    import doctest
    doctest.testmod()
