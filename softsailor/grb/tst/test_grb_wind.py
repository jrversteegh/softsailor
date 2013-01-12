import unittest
import testing_helper
from datetime import datetime, timedelta

from softsailor.utils import *

from softsailor.grb.grb_wind import *

class TestGrbWind(unittest.TestCase):
    def testAtlantic(self):
        w = GribWind(filename='Atlantic.wind.grb')
        d = datetime(year=2013, month=1, day=13, hour=18, minute=0)
        p = deg_to_rad((25, -55))
        w1 = w.get(p, d)
        d = datetime(year=2013, month=1, day=14, hour=12, minute=0)
        p = deg_to_rad((28, -79))
        w2 = w.get(p, d)
        self.assertAlmostEqual(316, rad_to_deg(w1[0]), delta=1.)
        self.assertAlmostEqual(19.2, ms_to_kn(w1[1]), delta=0.3)
        self.assertAlmostEqual(118, rad_to_deg(w2[0]), delta=1.)
        self.assertAlmostEqual(12.9, ms_to_kn(w2[1]), delta=0.3)

    def testKrys(self):
        w = GribWind(filename='KrysTransat.grb')
        d = datetime(year=2012, month=7, day=14, hour=6, minute=0)
        p = deg_to_rad((49, -19))
        w = w.get(p, d)
        self.assertAlmostEqual(325, rad_to_deg(w[0]), delta=1.)
        self.assertAlmostEqual(19, ms_to_kn(w[1]), delta=0.3)

if __name__ == '__main__':
    unittest.main()
