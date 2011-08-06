#!/usr/bin/env python2.7

"""
This scripts sets a new online wind_angle (TWA) for configured sol boat

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""

import sys, os, time, math
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

nwa = awa + 0.1
for i in (range(4)):
    if nwa < math.pi:
        steer(nwa * -mult)
        nwa += 0.1

nwa = 0.999 * math.pi
steer(nwa * -mult)
steer(nwa * mult)
nwa = awa + 0.4
for i in (range(4)):
    if nwa < math.pi:
        steer(nwa * mult)
    nwa -= 0.1
steer(awa * mult)
