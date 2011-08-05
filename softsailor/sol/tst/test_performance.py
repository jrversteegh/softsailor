import unittest
import math
import testing_helper

from softsailor.classes import PolarData

from softsailor.sol.sol_settings import Settings
from softsailor.sol.sol_performance import Performance

class TestPerformance(unittest.TestCase):
    def setUp(self):
        settings = Settings()
        self.perf = Performance(polar_data=settings.polar_data)
        
    def testGetOptimalAngles(self):
        angles = self.perf.get_optimal_angles(8.8)
        self.assertTrue(angles[0] > 0)
        self.assertTrue(angles[0] < math.pi * 0.333)
        self.assertTrue(angles[1] > math.pi * 0.666)
