import unittest
import testing_helper

from softsailor.boat import SailBoat 
from softsailor.sol.sol_functions import *

class TestSol(unittest.TestCase):
    @unittest.skipIf(testing_helper.offline, "Can't fetch boat offline")
    def testGetBoat(self):
        boat = SailBoat()
        boat.heading = -1
        fetch_boat(boat)
        self.assertTrue(boat.heading > 0, 'Test valid boat heading')

if __name__ == '__main__':
    unittest.main()
