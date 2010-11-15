#!/usr/bin/env python

"""
This script makes the configured sol boat simulate the supplied route

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""

import time
import sys
import os
from datetime import datetime, timedelta

args = sys.argv[1:]
if len(args) < 1:
    print "No route provided on commandline."
    exit(1)
else:
    route_file = args[0]

if not os.path.exists(route_file):
    print "Provided route: ", route_file, "doesn't exist."
    exit(1)
    
# Add softsailor to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from softsailor.sailor import Sailor
from softsailor.route import *
from softsailor.router import *

import softsailor.sol.sol_world
from softsailor.sol.sol_boat import Boat
from softsailor.updater import SimUpdater
from softsailor.controller import BoatController
from softsailor.sol.sol_functions import *

boat = Boat()
chart = get_map()
print "Map min lat: ", rad_to_deg(chart.minlat)
print "Map max lat: ", rad_to_deg(chart.maxlat)
print "Map min lon: ", rad_to_deg(chart.minlon)
print "Map max lon: ", rad_to_deg(chart.maxlon)

route = Route()
route.load_from_file(route_file)
print "Route:"
print route
route.save_to_kml('active_route.kml')
controller = BoatController(boat)
updater = SimUpdater(boat)
# Set boat at start of route
boat.position = route[0]
router = Router(boat=boat, route=route)

sailor = Sailor(boat=boat, router=router, map=chart, \
                controller=controller, updater=updater)

while sailor.sail():
    print "Waypoint      : ", router.active_index
    print "  Location    : ", router.active_waypoint
    bearing = router.active_waypoint.get_bearing_from(boat.position)
    print "  Bearing     : ", rad_to_deg(bearing[0])
    print "  Distance    : ", bearing[1] / 1852
    print "  Comment     : ", router.active_waypoint.comment
    print "  CTE         : ", router.get_cross_track() / 1852
    print "---"
    print "Boat time     : ", boat.situation.time
    print "Boat latitude : ", rad_to_deg(boat.position[0])
    print "Boat longitude: ", rad_to_deg(boat.position[1])
    print "Boat heading  : ", rad_to_deg(boat.heading)
    print "Boat course   : ", rad_to_deg(boat.motion.course)
    print "Boat speed    : ", ms_to_knots(boat.speed)
    print "Wind direction: ", rad_to_deg(boat.condition.wind[0])
    print "Wind angle    : ", rad_to_deg(boat.wind_angle)
    print "Wind speed    : ", ms_to_knots(boat.condition.wind[1])
    print "Apparent angle: ", rad_to_deg(boat.apparent_wind.sa)
    print "Apparent speed: ", ms_to_knots(boat.apparent_wind[1])
    print "---"
    sailor.print_log()
    print "==="
    sys.stdout.flush()
    sys.stderr.flush()

updater.save_log("track_log")
sailor.save_log("sail_log")

print "Route completed!"