# -*- coding: utf-8 -*-

from pyredux.internal.store import Store
from pyredux.internal.params import __INIT


def create(reducer, initial_state):
    """
    Create a new store to contain state. Only one should be used per
    application.

    Args:
        reducer: A callable that will accept two arguments: state and action
        initial_state: The initial state for this store. Can be any type.

    Returns:
        A store object with dispatch, get_state, replace_reducer
        and subscribe functions.
    """
    if not callable(reducer):
        raise TypeError

    _state = {"current_reducer": reducer,
              "current_state": initial_state,
              "listeners": [],
              "is_dispatching": False}

    def get_state():
        """
        Get the current state from the store.

        Returns:
            The current state of the store
        """
        return _state["current_state"]

    def subscribe(listener):
        """

        Args:
            listener: Callable which will accept two callables
                (dispatch, get_state). These can be used to dispatch new
                actions and retrieve the current state.

        Returns:
            callable: An unsubscribe function to unsubscribe
            the given listener.
        """
        _state["listeners"].append(listener)

        state = {"is_subscribed": True}

        def unsubscribe():
            """
            Un-subscibe the previously subscribed listener.
            This function can be called multiple times, but will only
            return False when any action was taken.

            Returns:
                bool: True or False depending on if any action was taken.
            """

            if not state["is_subscribed"]:
                return False

            state["is_subscribed"] = False

            try:
                _state["listeners"].remove(listener)
            except ValueError:
                return False

            return True

        return unsubscribe

    def dispatch(action):
        """
        Dispatch the given action by calling the reducer and firing the
        listeners when complete.

        Args:
            action: A dict(-like) with a type key.
                Can contain more keys, but type is required.

        Returns:
            The action that was passed to the dispatcher
        """

        if not isinstance(action, dict):
            raise TypeError

        if not action.get('type'):
            raise TypeError

        if _state["is_dispatching"]:
            raise RuntimeError

        try:
            state = _state['current_state']
            _reducer = _state['current_reducer']

            _state["is_dispatching"] = True
            _state["current_state"] = _reducer(state, action)
        finally:
            _state["is_dispatching"] = False

        for listener in _state["listeners"]:
            listener(dispatch, get_state)

        return action

    def replace_reducer(next_reducer):
        """
        Replace the current reducer used by the store with a different one

        Args:
            next_reducer: The reducer to replace the current reducer with
        """
        _state["current_reducer"] = next_reducer
        dispatch({"type": __INIT})

    dispatch({"type": __INIT})

    return Store({"dispatch": dispatch,
                  "get_state": get_state,
                  "replace_reducer": replace_reducer,
                  "subscribe": subscribe})
