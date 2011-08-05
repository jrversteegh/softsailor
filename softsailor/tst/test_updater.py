#!/usr/bin/env python

import math
import unittest
import tempfile
from datetime import datetime, timedelta

import testing_helper

from softsailor.updater import *
from softsailor.boat import SailBoat

class TestUpdater(unittest.TestCase):
    def setUp(self):
        self.boat = SailBoat()
        self.boat.position = (1.0, 1.0)
        self.boat.speed = 5
        self.boat.heading = math.pi
        self.updater = BoatUpdater(self.boat)

    def TestUpdate(self):
        self.updater.update()

    def TestSaveLog(self):
        self.updater.update()
        for i in range(1, 1000):
            self.boat.position = (1.0 - 0.0001 * i, 1.0)
            self.boat.speed = 5 + math.sin(0.05 * i) 
            self.boat.time += timedelta(minutes=1)
            self.updater.update()
        self.updater.save_log(tempfile.gettempdir() + '/test_log')

if __name__ == '__main__':
    unittest.main()
