import unittest
from unittest.mock import MagicMock, ANY
from pyredux import compose


class ComposeTest(unittest.TestCase):

    def testShouldReturnArgumentWhenNothingToCompose(self):
        expected = 1

        composed = compose()
        actual = composed(expected)

        self.assertEqual(actual, expected)

    def testShouldComposeFunctions(self):
        value = 1

        def func1(param):
            self.assertEqual(param, value)
            return param

        def func2(param):
            self.assertEqual(param, value)
            return param

        composed = compose(func1, func2)
        self.assertTrue(callable(composed))

        composed(value)
