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

settings = get_settings()
if settings.map == '':
    area = settings.area
    print "Map tiles     : ", settings.tilemap, \
        lat_to_str(area[0]), lat_to_str(area[1]), \
        lon_to_str(area[2]), lon_to_str(area[3])
else:
    print "Map           : ", settings.map

print "Weather       : ", settings.weather

print "Boat latitude : ", lat_to_str(boat.position[0])
print "Boat longitude: ", lon_to_str(boat.position[1])
print "Boat heading  : ", ang_to_str(boat.heading)
print "Boat course   : ", ang_to_str(boat.motion.course)
print "Boat speed    : ", spd_to_str(boat.speed)
print "Wind direction: ", ang_to_str(boat.condition.wind[0])
print "Wind angle    : ", ang_to_str(boat.wind_angle)
print "Wind speed    : ", spd_to_str(boat.condition.wind[1])
print "Apparent angle: ", ang_to_str(normalize_angle_pipi(boat.apparent_wind[0]))
print "Apparent speed: ", spd_to_str(boat.apparent_wind[1])
