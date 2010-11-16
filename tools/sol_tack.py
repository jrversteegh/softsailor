#!/usr/bin/env python

"""
This scripts tacks the configured sol boat

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""

import sys, os, time
# Add softsailor to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from softsailor.utils import *
from softsailor.boat import SailBoat
from softsailor.sol.sol_functions import fetch_boat, do_steer_wind


boat = SailBoat()
fetch_boat(boat)

print "Boat latitude  : ", rad_to_deg(boat.position[0])
print "Boat longitude : ", rad_to_deg(boat.position[1])
print "Boat wind angle: ", rad_to_deg(boat.wind_angle)
print "Boat speed     : ", ms_to_kn(boat.speed)

wa = boat.wind_angle
awa = abs(wa)
mult = 1
if wa >= 0:
    mult = -1

# When it's blowing hard or we're down on efficiency, turn the boat into the wind first
if (boat.efficiency < 0.98) or (boat.condition.wind[1] > 8):
    print "Turning into the wind",
    sys.stdout.flush()
    do_steer_wind(0)
    while boat.speed > 0.01:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1)
        fetch_boat(boat)
    print " Done."
    print "Boat efficiency : ", boat.efficiency
    print "Waiting for 100% efficiency",
    sys.stdout.flush()
    while boat.efficiency < 0.999:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1)
        fetch_boat(boat)
    print " Done."
 
def steer(a):
    print "Steering wind angle: ", round(rad_to_deg(a), 2),
    sys.stdout.flush()
    do_steer_wind(a)
    while abs(boat.wind_angle - a) > 0.001:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1)
        fetch_boat(boat)
    print " Done."
    time.sleep(10)

steer(awa * mult)
