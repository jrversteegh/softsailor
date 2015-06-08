import unittest
import math
import testing_helper
import timeit
from datetime import datetime, timedelta
import numpy as np


from softsailor.vr.vr_settings import Settings
from softsailor.vr.vr_performance import Performance


class TestPerformance(unittest.TestCase):
    @unittest.skipIf(testing_helper.offline, "Can't get boat performance offline")
    def testGetOptimalAngles(self):
        pass

    def testCompareWithPolar(self):
        pass

    def testCompareWithPolarAtMesh(self):
        pass

    def testPerformance(self):
        pass




if __name__ == '__main__':
    unittest.main()
