#!/usr/bin/env python2.7

"""
This script makes the configured sol boat follow the supplied route

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
from softsailor.sailor import Sailor
from softsailor.route import *
from softsailor.navigator import *

from softsailor.sol.sol_boat import SolBoat
from softsailor.sol.sol_updater import SolUpdater
from softsailor.sol.sol_controller import Controller
from softsailor.sol.sol_functions import *

boat = SolBoat()
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
controller = Controller(boat)
updater = SolUpdater(boat)
# Update now so the boat has a proper initial position
updater.update()
navigator = Navigator(boat=boat, route=route)
course = get_course()

sailor = Sailor(boat=boat, navigator=navigator, chart=chart, \
                controller=controller, updater=updater, course=course)

logged = datetime.utcnow()

while sailor.sail():
    print "Waypoint      : ", navigator.active_index
    print "  Location    : ", pos_to_str(navigator.active_leg[1])
    bearing = navigator.active_leg[1] - boat.position
    print "  Bearing     : ", ang_to_str(bearing[0])
    print "  Distance    : ", dst_to_str(bearing[1])
    print "  Comment     : ", navigator.active_leg[1].comment
    print "  CTE         : ", dst_to_str(navigator.get_cross_track())
    print "---"
    print "Boat time     : ", boat.situation.time.strftime(time_format)
    print "Boat latitude : ", lat_to_str(boat.position[0])
    print "Boat longitude: ", lon_to_str(boat.position[1])
    print "Boat heading  : ", ang_to_str(boat.heading)
    print "Boat course   : ", ang_to_str(boat.motion.course)
    print "Boat speed    : ", spd_to_str(boat.speed)
    print "Wind direction: ", ang_to_str(boat.condition.wind.a)
    print "Wind angle    : ", ang_to_str(boat.wind_angle)
    print "Wind speed    : ", spd_to_str(boat.condition.wind.r)
    print "Apparent angle: ", ang_to_str(normalize_angle_pipi(boat.apparent_wind.a))
    print "Apparent speed: ", spd_to_str(boat.apparent_wind.r)
    print "---"
    sailor.print_log(5)
    print "==="
    sys.stdout.flush()
    sys.stderr.flush()
    if datetime.utcnow() - logged > timedelta(minutes=10):
        updater.save_log("track_log")
        sailor.save_log("sail_log")
        logged = datetime.utcnow()
    sleep(10)

print "Route completed!"
