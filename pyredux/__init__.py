from functools import reduce


def compose(*funcs):

    def wrapped(*args):
        if not len(funcs):
            return args[0]

        last = funcs[-1]
        rest = funcs[:-1]

        return reduce(lambda composed, f: f(composed), reversed(rest),
                      last(*args))

    return wrapped


__all__ = ["store", "middleware"]
