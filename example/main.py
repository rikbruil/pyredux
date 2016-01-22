from pyredux.store import create

state = 0


def reducer(state, action):
    print("trigger reducer")
    return state + 1


def listener(dispatch, get_state):
    print("Listener fired!")
    return


store = create(reducer, state)
store.subscribe(listener)

store.dispatch({"type": "foo"})
