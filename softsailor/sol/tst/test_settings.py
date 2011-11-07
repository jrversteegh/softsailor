import unittest
import testing_helper

from softsailor.sol.sol_settings import *

import os
import math

class TestSolSettings(unittest.TestCase):
    def setUp(self):
        os.chdir('/')
        self.settings = Settings()
    @unittest.skipIf(testing_helper.offline, "Can't get settings offline")
    def testLoadSettings(self):
        self.assertTrue(self.settings.host == 'race.sailport.se')
        self.assertTrue(self.settings.token != '')
        self.assertTrue(self.settings.race != '')
        self.assertTrue(self.settings.boat != '')
        self.assertTrue(self.settings.weather != '')
        if self.settings.tilemap != '':
            self.assertTrue(self.settings.area[0] > (-0.49 * math.pi))
            self.assertTrue(self.settings.area[1] < (0.49 * math.pi))
            self.assertTrue(self.settings.area[2] > (-0.99 * math.pi))
            self.assertTrue(self.settings.area[3] < (0.99 * math.pi))
    @unittest.skipIf(testing_helper.offline, "Can't get settings offline")
    def testPolarData(self):
        self.assertTrue(len(self.settings.polar_data.angles) > 0)
        self.assertEqual(len(self.settings.polar_data.angles), \
                len(self.settings.polar_data.data))

if __name__ == '__main__':
    unittest.main()
