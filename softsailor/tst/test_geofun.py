#!/usr/bin/env python

import unittest
import testing_helper

from geofun import Position, Line

class TestLine(unittest.TestCase):
    def test_line_doesnt_self_intersect(self):
        p1 = Position(0.0, 0.0)
        p2 = Position(0.1, 0.1)
        l1 = Line(p1, p2)
        l2 = Line(p1, p2)
        l3 = Line(p2, p1)
        self.assertFalse(l1.intersects(l2))
        self.assertFalse(l1.intersects(l3))
        self.assertFalse(l3.intersects(l1))

    def test_line_doesnt_intersect_at_end(self):
        p1 = Position(0.0, 0.0)
        p2 = Position(0.1, 0.1)
        p3 = Position(0.1, 0.0)
        l1 = Line(p1, p2)
        l2 = Line(p1, p3)
        l3 = Line(p3, p1)
        l4 = Line(p3, p2)
        self.assertFalse(l1.intersects(l2))
        self.assertFalse(l1.intersects(l3))
        self.assertFalse(l1.intersects(l4))
        self.assertFalse(l2.intersects(l1))
        self.assertFalse(l3.intersects(l1))
        self.assertFalse(l3.intersects(l1))
        self.assertFalse(l4.intersects(l1))

if __name__ == '__main__':
    unittest.main()

