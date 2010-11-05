#!/usr/bin/env python

import unittest

from softsailor.controller import Controller

class TestController(unittest.TestCase):
    def setUp(self):
        self.controller = Controller()

    def TestSteerHeading(self):
        self.controller.steer_heading(3.14)

    def TestSteerWindAngle(self):
        self.controller.steer_wind_angle(1.57)


if __name__ == '__main__':
    unittest.main()
