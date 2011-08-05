
import unittest
import testing_helper

from motion import Motion

class TestMotion(unittest.TestCase):
    def setUp(self):
        self.motion = Motion((0, 0))

    def testHasSpeed(self):
        self.assertTrue(hasattr(self.motion, 'speed'))

    def testHasVelocity(self):
        self.assertTrue(hasattr(self.motion, 'velocity'))
        try:
            it = iter(self.motion.velocity)
        except TypeError:
            self.fail('Velocity iterable check')


if __name__ == '__main__':
    unittest.main()
