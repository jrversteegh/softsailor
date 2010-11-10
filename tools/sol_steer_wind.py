#!/usr/bin/env python

"""
This scripts sets a new online wind_angle (TWA) for configured sol boat

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
print "Boat speed     : ", ms_to_knots(boat.speed)

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

args = sys.argv[1:]
if len(args) < 1:
    print "No new wind angle provided on commandline."
elif len(args) < 2:
    new_wind_angle = float(args[0])
    print "Steering       : ", new_wind_angle, " degrees."
    rad_wind_angle = deg_to_rad(new_wind_angle)
    do_steer_wind(rad_wind_angle)
    # Sleep 10s so sailonline can process the request
    time.sleep(10)
    fetch_boat(boat)
    print "New wind angle : ", rad_to_deg(boat.wind_angle)
else:
    new_wind_angle = deg_to_rad(float(args[0]))
    step = deg_to_rad(float(args[1]))
    diff = normalize_angle_pipi(new_wind_angle - boat.wind_angle)
    mult = 1
    if diff < 0:
        mult = -1
    while abs(diff) > step:
        steer(boat.wind_angle + step * mult)
        diff = normalize_angle_pipi(new_wind_angle - boat.wind_angle)
    steer(new_wind_angle)


