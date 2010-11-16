#!/usr/bin/env python

"""
This script sets a new online heading (CC) for configured sol boat

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""

import sys, os, time
# Add softsailor to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from softsailor.utils import *
from softsailor.boat import SailBoat
from softsailor.sol.sol_functions import fetch_boat, do_steer


boat = SailBoat()
fetch_boat(boat)

print "Boat latitude : ", rad_to_deg(boat.position[0])
print "Boat longitude: ", rad_to_deg(boat.position[1])
print "Boat heading  : ", rad_to_deg(boat.heading)
print "Boat speed    : ", ms_to_kn(boat.speed)

args = sys.argv[1:]
if len(args) < 1:
    print "No new heading provided on commandline."
else:
    new_heading = args[0]
    print "Steering      : ", new_heading, " degrees."
    rad_heading = deg_to_rad(new_heading)
    do_steer(rad_heading)
    # Sleep 10s so sailonline can process the request
    time.sleep(10)
    fetch_boat(boat)
    print "New heading   : ", rad_to_deg(boat.heading)
