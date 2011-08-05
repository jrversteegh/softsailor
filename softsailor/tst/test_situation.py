
import unittest
import testing_helper

from softsailor.situation import Situation

class TestSituation(unittest.TestCase):
    def setUp(self):
        self.situation = Situation()

    def testHasHeading(self):
        self.assertTrue(hasattr(self.situation, 'heading'))

    def testHasTime(self):
        self.assertTrue(hasattr(self.situation, 'time'))

    def testHasPosition(self):
        try:
            it = iter(self.situation.position)
        except TypeError:
            self.fail('Position iterable check')


if __name__ == '__main__':
    unittest.main()
