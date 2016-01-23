# -*- coding: utf-8 -*-


class BaseStore:
    _store = None

    def __init__(self, store):
        self._store = store

    def dispatch(self, action):
        return self._store['dispatch'](action)

    def get_state(self):
        return self._store['get_state']()


class Store(BaseStore):
    _store = None

    def __init__(self, store):
        self._store = store
        BaseStore.__init__(self, store)

    def subscribe(self, listener):
        return self._store['subscribe'](listener)

    def replace_reducer(self, reducer):
        return self._store['replace_reducer'](reducer)
