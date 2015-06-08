import unittest
import math
import testing_helper
import timeit
from datetime import datetime, timedelta
import numpy as np


from softsailor.sol.sol_settings import Settings
from softsailor.sol.sol_performance import Performance

settings = Settings()
polars=settings.polars
perf = Performance(polars=polars)

def test_polar():
    angles = np.linspace(1, 2, 20)
    for i in xrange(50000):
       polars.get(angles, 8.8)

def test_perf():
    for i in xrange(50000):
       perf.get((1.1, 8.8))

class TestPerformance(unittest.TestCase):
    @unittest.skipIf(testing_helper.offline, "Can't get boat performance offline")
    def testGetOptimalAngles(self):
        angles = perf.get_optimal_angles(8.8)
        self.assertTrue(angles[0] > 0)
        self.assertTrue(angles[0] < math.pi * 0.333)
        self.assertTrue(angles[1] > math.pi * 0.666)

    def testCompareWithPolar(self):
        v11 = polars.get([0.9, 1.0, 1.1, 1.2], 8.0)
        v12 = polars.get([0.9, 1.0, 1.1, 1.2], 10.5)
        v211 = perf.get((0.9, 8.0))[1]
        v212 = perf.get((1.0, 8.0))[1]
        v213 = perf.get((1.1, 8.0))[1]
        v214 = perf.get((1.2, 8.0))[1]
        v221 = perf.get((0.9, 10.5))[1]
        v222 = perf.get((1.0, 10.5))[1]
        v223 = perf.get((1.1, 10.5))[1]
        v224 = perf.get((1.2, 10.5))[1]
        self.assertAlmostEqual(v11[0], v211, delta=0.05)
        self.assertAlmostEqual(v11[1], v212, delta=0.05)
        self.assertAlmostEqual(v11[2], v213, delta=0.05)
        self.assertAlmostEqual(v11[3], v214, delta=0.05)
        self.assertAlmostEqual(v12[0], v221, delta=0.05)
        self.assertAlmostEqual(v12[1], v222, delta=0.05)
        self.assertAlmostEqual(v12[2], v223, delta=0.05)
        self.assertAlmostEqual(v12[3], v224, delta=0.05)

    def testCompareWithPolarAtMesh(self):
        a = polars.wind_angles[50]
        w = polars.wind_speeds[20]
        s = polars._data[50, 20]
        v1 = polars.get(a, w)
        v2 = perf.get((a, w))[1]
        self.assertAlmostEqual(s, v2, delta=0.02)
        self.assertAlmostEqual(s, v1, delta=0.02)

    def testPerformance(self):
        t1 = datetime.now()
        test_polar()
        t2 = datetime.now()
        test_perf()
        t3 = datetime.now()
        self.assertTrue((t2 - t1).total_seconds() < 1)
        self.assertTrue((t3 - t2).total_seconds() < 2)



if __name__ == '__main__':
    unittest.main()
