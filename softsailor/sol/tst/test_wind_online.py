#!/usr/bin/env python

import unittest
import testing_helper

from softsailor.utils import *

from softsailor.sol.sol_wind import *
from softsailor.sol.sol_weather import *
from softsailor.sol.sol_settings import *

from datetime import datetime, timedelta

class TestWindOnline(unittest.TestCase):
    def setUp(self):
        settings = Settings()
        self.weather = Weather()
        self.weather.load(settings)
        self.wind = SolWind(self.weather)

    def tearDown(self):
        self.wind = None
        self.weather = None

    def testBoatWind(self):
        pass

if __name__ == '__main__':
    unittest.main()
