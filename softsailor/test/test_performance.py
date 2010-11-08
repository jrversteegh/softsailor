import unittest

from softsailor.performance import *

class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.performance = Performance(0)

    def testHasGet(self):
        self.assertTrue(hasattr(self.performance, 'get'))
        self.assertTrue(hasattr(self.performance.get, '__call__'))

    def testHasGetOptimalAngles(self):
        self.assertTrue(hasattr(self.performance, 'get_optimal_angles'))
        self.assertTrue(hasattr(self.performance.get_optimal_angles, '__call__'))
