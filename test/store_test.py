import unittest
from pyredux.store import create


class StoreTest(unittest.TestCase):

    @staticmethod
    def reducer(state, action):
        return state + 1

    def testShouldHandleCreate(self):
        state = 1
        store = create(self.reducer, state)

        self.assertEqual(store.get_state(), state + 1)

    def testShouldRaiseTypeExceptionOnInvalidActionType(self):
        action = {}
        state = 1
        store = create(self.reducer, state)

        with self.assertRaises(TypeError):
            store.dispatch('foo')

        with self.assertRaises(TypeError):
            store.dispatch(action)

    def testShouldRaiseTypeExceptionOnInvalidReducerType(self):
        state = 1
        with self.assertRaises(TypeError):
            create("foo", state)

    def testShouldRaiseExceptionWhenAlreadyDispatching(self):
        _state = 1
        _store = {"store": create(self.reducer, _state)}
        store = _store["store"]

        def reducer(state, action):
            store.dispatch(action)
            return state

        with self.assertRaises(RuntimeError):
            store.replace_reducer(reducer)

    def listener(self, dispatch, get_state):
        self.assertTrue(callable(dispatch))
        self.assertTrue(callable(get_state))

    def testShouldFireListenerOnDispatch(self):
        state = 0

        store = create(self.reducer, state)
        unsubscribe = store.subscribe(self.listener)
        self.assertTrue(callable(unsubscribe))

        store.dispatch({"type": "foo"})

        self.assertTrue(unsubscribe())
        self.assertFalse(unsubscribe())
