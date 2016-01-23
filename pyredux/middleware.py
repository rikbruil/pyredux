# -*- coding: utf-8 -*-

from pyredux import compose


def apply(*middlewares):

    def iterate(other):

        def wrap(reducer, initial_state):
            store = other(reducer, initial_state)
            dispatch = store.dispatch
            api = {"dispatch": lambda action: dispatch(action),
                   "get_state": store.get_state}

            chain = map(lambda middleware: middleware(api), middlewares)
            dispatch = compose(*chain)(store.dispatch)

            store.dispatch = dispatch

            return store

        return wrap

    return iterate
