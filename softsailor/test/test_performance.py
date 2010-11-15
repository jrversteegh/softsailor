import unittest

from softsailor.performance import *

class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.performance = Performance(0)

    def testHasGet(self):
        self.assertTrue(hasattr(self.performance, 'get'))
        self.assertTrue(hasattr(self.performance.get, '__call__'))
        
    def testHasGetSpeed(self):
        self.assertTrue(hasattr(self.performance, 'get_speed'))
        self.assertTrue(hasattr(self.performance.get_speed, '__call__'))

    def testHasGetDrift(self):
        self.assertTrue(hasattr(self.performance, 'get_drift'))
        self.assertTrue(hasattr(self.performance.get_drift, '__call__'))

    def testHasGetOptimalAngles(self):
        self.assertTrue(hasattr(self.performance, 'get_optimal_angles'))
        self.assertTrue(hasattr(self.performance.get_optimal_angles, '__call__'))
