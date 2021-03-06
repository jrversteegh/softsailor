#!/usr/bin/env python2.7

"""
This script makes the configured sol boat simulate the supplied route

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""

from time import sleep
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

from softsailor.utils import *
from softsailor.classes import *
from softsailor.sailor import Sailor
from softsailor.route import *
from softsailor.navigator import *

import softsailor.sol.sol_world
from softsailor.sol.sol_boat import Boat
from softsailor.sol.sol_updater import SimUpdater
from softsailor.controller import BoatController
from softsailor.sol.sol_functions import *

boat = Boat()
chart = get_chart()
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
navigator = Navigator(boat=boat, route=route)

sailor = Sailor(boat=boat, navigator=navigator, chart=chart, \
                controller=controller, updater=updater)

sleep(2)
i = 0
while sailor.sail():
    if i % 50 == 0:
        print boat.time.strftime(time_format), \
                vel_to_str(boat.motion.velocity)
        # For checking exceptions...
        #sailor.print_log()
    i += 1
    sys.stdout.flush()

print '%d steps' % i

print boat.time.strftime(time_format), \
        pos_to_str(boat.situation.position), \
        ang_to_str(boat.wind_angle), \
        vel_to_str(boat.motion.velocity)

updater.save_log("track.log")
updater.save_to_kml("track.kml")
sailor.save_log("sail.log")

print "Route completed!"
