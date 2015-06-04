import unittest
import testing_helper

from softsailor.vr.vr_settings import *

import os
import math

class TestVrSettings(unittest.TestCase):
    def setUp(self):
        os.chdir('/')
        self.settings = Settings()
    @unittest.skipIf(testing_helper.offline, "Can't get settings offline")
    def testLoadSettings(self):
        self.assertTrue(self.settings.host == 'vvor.virtualregatta.com')
        self.assertTrue(self.settings.user != '')
        self.assertTrue(self.settings.key != '')
    @unittest.skipIf(testing_helper.offline, "Can't get settings offline")
    def testPolarData(self):
        self.assertTrue(len(self.settings.polars) > 0)

if __name__ == '__main__':
    unittest.main()
