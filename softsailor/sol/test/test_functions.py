import unittest

from softsailor.boat import SailBoat 
from softsailor.sol.functions import *

class TestSol(unittest.TestCase):
    def testGetBoat(self):
        boat = SailBoat()
        boat.heading = -1
        get_boat(boat)
        self.assertTrue(boat.heading > 0, 'Test valid boat heading')

