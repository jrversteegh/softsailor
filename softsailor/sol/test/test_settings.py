import unittest

from softsailor.sol.settings import *

import os

class TestSolSettings(unittest.TestCase):
    def setUp(self):
        os.chdir('/')
        self.settings = Settings()
    def testLoadSettings(self):
        self.assertTrue(self.settings.host == 'race.sailport.se')
        self.assertTrue(self.settings.token != '')
        self.assertTrue(self.settings.race != '')
        self.assertTrue(self.settings.boat != '')
        self.assertTrue(self.settings.weather != '')
        self.assertTrue(self.settings.map != '')
    def testPolarData(self):
        self.assertTrue(len(self.settings.polar_data.angles) > 0)
        self.assertEqual(len(self.settings.polar_data.angles), \
                len(self.settings.polar_data.data))

if __name__ == '__main__':
    unittest.main()
