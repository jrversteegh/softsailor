#!/usr/bin/env python

"""
This scripts prints the status of the currently configured sol boat

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""

import sys, os
# Add softsailor to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from softsailor.utils import *
from softsailor.boat import SailBoat
from softsailor.sol.sol_functions import get_boat

boat = SailBoat()
get_boat(boat)

print "Boat latitude : ", rad_to_deg(boat.position[0])
print "Boat longitude: ", rad_to_deg(boat.position[1])
print "Boat heading  : ", rad_to_deg(boat.heading)
print "Boat course   : ", rad_to_deg(boat.motion.course)
print "Boat speed    : ", ms_to_knots(boat.speed)
print "Wind direction: ", rad_to_deg(boat.condition.wind[0])
print "Wind angle    : ", rad_to_deg(boat.wind_angle)
print "Wind speed    : ", ms_to_knots(boat.condition.wind[1])
print "Apparent angle: ", rad_to_deg(boat.apparent_wind[0])
print "Apparent speed: ", ms_to_knots(boat.apparent_wind[1])
