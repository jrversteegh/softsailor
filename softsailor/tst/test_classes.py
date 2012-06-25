import unittest
import math

import testing_helper
from softsailor.classes import *

class TestPath(unittest.TestCase):
    def setUp(self):
        self.p1 = Position(0.9, 0.9)
        self.p2 = Position(0.9, 1.0)
        self.p3 = Position(1.0, 1.0)
        l = [self.p1, self.p2, self.p3]
        self.p = Path(l)

    def test_construction(self):
        self.assertEquals(3, len(self.p))
        s1 = Line(self.p1, self.p2)
        s2 = Line(self.p2, self.p3)
        le = s1.v.r + s2.v.r
        self.assertEquals(le, self.p.length)

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

    def test_segments(self):
        i = 0
        l = 0
        for s in self.p.segments:
            l += s.v.r
            i += 1
        self.assertEquals(2, i)
        self.assertEquals(self.p.length, l)




if __name__ == '__main__':
    unittest.main()

