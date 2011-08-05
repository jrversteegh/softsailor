#!/usr/bin/env python

import unittest
import testing_helper

from softsailor.world import World

class TestWorld(unittest.TestCase):
    def setUp(self):
        self.world = World()

    def TestHasWind(self):
        self.assertTrue(hasattr(self.world, 'wind'))
        self.assertTrue(hasattr(self.world.wind, 'get'))

    def TestHasCurrent(self):
        self.assertTrue(hasattr(self.world, 'current'))
        self.assertTrue(hasattr(self.world.current, 'get'))

    def TestHasLand(self):
        self.assertTrue(hasattr(self.world, 'land'))
        self.assertTrue(hasattr(self.world.land, 'hit'))


if __name__ == '__main__':
    unittest.main()
