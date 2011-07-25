#!/usr/bin/env python

"""
This scripts prints the status of the currently configured sol boat

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""

import sys, os
# Add softsailor to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from softsailor.utils import *
from softsailor.boat import SailBoat
from softsailor.sol.sol_functions import fetch_boat, get_settings

boat = SailBoat()
fetch_boat(boat)

print "Map           : ", get_settings().map
print "Weather       : ", get_settings().weather

print "Boat latitude : ", u"%10.4f\u00B0N".encode('utf-8') \
        % rad_to_deg(boat.position[0])
print "Boat longitude: ", u"%10.4f\u00B0E".encode('utf-8') \
        % rad_to_deg(boat.position[1])
print "Boat heading  : ", u"%10.2f\u00B0".encode('utf-8') \
        % rad_to_deg(boat.heading)
print "Boat course   : ", u"%10.2f\u00B0".encode('utf-8') \
        % rad_to_deg(boat.motion.course)
print "Boat speed    : ", "%10.2f kn" % ms_to_kn(boat.speed)
print "Wind direction: ", u"%10.2f\u00B0".encode('utf-8') \
        % rad_to_deg(boat.condition.wind[0])
print "Wind angle    : ", u"%10.2f\u00B0".encode('utf-8') \
        % rad_to_deg(boat.wind_angle)
print "Wind speed    : ", "%10.2f kn" % ms_to_kn(boat.condition.wind[1])
print "Apparent angle: ", u"%10.2f\u00B0".encode('utf-8') \
        % rad_to_deg(normalize_angle_pipi(boat.apparent_wind[0]))
print "Apparent speed: ", "%10.2f kn" % ms_to_kn(boat.apparent_wind[1])
