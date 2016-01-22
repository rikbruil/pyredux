from pyredux import compose


def apply(*middlewares):

    def iterate(next):

        def wrap(reducer, initialState):
            store = next(reducer, initialState)
            dispatch = store.dispatch
            api = {"dispatch": lambda action: dispatch(action),
                   "get_state": store.get_state}

            chain = map(lambda middleware: middleware(api), middlewares)
            dispatch = compose(*chain)(store.dispatch)

            store.dispatch = dispatch

            return store

        return wrap

    return iterate
