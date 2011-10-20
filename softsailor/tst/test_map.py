#!/usr/bin/env python

import unittest
import testing_helper

from geofun import Position, Line

from softsailor.map import *

class TestPath(unittest.TestCase):
    def test_construction(self):
        p1 = Position(0.9, 0.9)
        p2 = Position(0.9, 1.0)
        p3 = Position(1.0, 1.0)
        l = [p1, p2, p3]
        p = Path(l)
        self.assertEquals(3, len(p))
        s1 = Line(p1, p2)
        s2 = Line(p2, p3)
        le = s1.v.r + s2.v.r
        self.assertEquals(le, p.length)

    def test_comparison(self):
        p1a = Position(0.88, 0.88)
        p1b = Position(0.9, 0.9)
        p2 = Position(0.9, 1.0)
        p3 = Position(1.0, 1.0)
        l1 = [p1a, p2, p3]
        l2 = [p1b, p2, p3]
        self.assertTrue(l1 < l2)
        self.assertFalse(l1 > l2)
        p1 = Path(l1)
        p2 = Path(l2)
        self.assertTrue(p1 > p2)
        self.assertFalse(p1 < p2)


class TestMap(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
