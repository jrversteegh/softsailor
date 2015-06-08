#!/usr/bin/env python

import unittest
import testing_helper

from softsailor.utils import *

from softsailor.vr.vr_wind import *
from softsailor.vr.vr_weather import *
from softsailor.vr.vr_settings import *

from datetime import datetime, timedelta

class TestWindOnline(unittest.TestCase):
    def setUp(self):
        settings = Settings()
        self.weather = Weather()
        self.weather.load(settings)
        self.wind = Wind(self.weather)

    def tearDown(self):
        self.wind = None
        self.weather = None


    @unittest.skipIf(testing_helper.offline, "Can't get wind and boat offline")
    def testBoatWind(self):
        pass

if __name__ == '__main__':
    unittest.main()
