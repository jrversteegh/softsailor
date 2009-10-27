import unittest
import math

from softsailor.classes import PolarData

from softsailor.sol.settings import Settings
from softsailor.sol.performance import Performance

class TestPerformance(unittest.TestCase):
    def setUp(self):
        settings = Settings()
        self.perf = Performance(settings.polar_data)
        
    def testOptimalAngles(self):
        angles = self.perf.optimal_angles(8.8)
        self.assertTrue(angles[0] > 0)
        self.assertTrue(angles[0] < math.pi * 0.333)
        self.assertTrue(angles[1] > math.pi * 0.666)
