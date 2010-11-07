#!/usr/bin/env python

import unittest

from softsailor.updater import *
from softsailor.boat import SailBoat

class TestUpdater(unittest.TestCase):
    def setUp(self):
        self.boat = SailBoat()
        self.updater = BoatUpdater(self.boat)

    def TestUpdate(self):
        self.updater.update()

if __name__ == '__main__':
    unittest.main()
