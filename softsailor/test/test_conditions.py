
import unittest

from conditions import Condition, Conditions

class TestCondition(unittest.TestCase):
    def setUp(self):
        self.condition = Condition((0, 0), (0, 0))

    def testHasWind(self):
        self.assertTrue(hasattr(self.condition, 'wind'))
        try:
            it = iter(self.condition.wind)
        except TypeError:
            self.fail('Wind iterable check')

    def testHasCurrent(self):
        self.assertTrue(hasattr(self.condition, 'current'))
        try:
            it = iter(self.condition.current)
        except TypeError:
            self.fail('Current iterable check')

class TestConditions(unittest.TestCase):
    def setUp(self):
        self.conditions = Conditions()

    def testHasGetWind(self):
        self.conditions.get_wind(0, 0)

    def testHasGetCurrent(self):
        self.conditions.get_current(0, 0)

    def testHasGetCondition(self):
        self.conditions.get_condition(0, 0)

if __name__ == '__main__':
    unittest.main()
