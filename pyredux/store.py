from pyredux.internal.store import Store
from pyredux.internal.paramTypes import __INIT


def create(reducer, initial_state):
    if not callable(reducer):
        raise TypeError

    _state = {"current_reducer": reducer,
              "current_state": initial_state,
              "listeners": [],
              "is_dispatching": False}

    def get_state():
        return _state["current_state"]

    def subscribe(listener):
        _state["listeners"].append(listener)

        state = {"is_subscribed": True}

        def unsubscribe():
            if not state["is_subscribed"]:
                return False

            state["is_subscribed"] = False

            try:
                _state["listeners"].remove(listener)
            finally:
                return True

        return unsubscribe

    def dispatch(action):
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
        _state["current_reducer"] = next_reducer
        dispatch({"type": __INIT})

    dispatch({"type": __INIT})

    return Store({"dispatch": dispatch,
                  "get_state": get_state,
                  "replace_reducer": replace_reducer,
                  "subscribe": subscribe})
