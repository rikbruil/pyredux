# -*- coding: utf-8 -*-
"""Pyredux module

This module is a port of the JavaScript Redux project.
"""

from functools import reduce


def compose(*funcs):
    """
    Compose two or more callables together.

    Args:
        *funcs: List of callables to be composed

    Returns:
        Newly created callable
    """

    def wrapped(*args):
        """
        Newly created function which wraps the originally passed functions.

        Args:
            *args: The original arguments the functions would receive.

        Returns:
            Depends on the originally passed functions if this would return
            anything or not.
        """
        if not len(funcs):
            return args[0]

        last = funcs[-1]
        rest = funcs[:-1]

        return reduce(lambda composed, f: f(composed), reversed(rest),
                      last(*args))

    return wrapped


__all__ = ["store", "middleware"]
