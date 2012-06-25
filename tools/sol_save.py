#!/usr/bin/env python2.7

"""
This scripts saves the course and map of the currently configured race to kml

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""

import sys, os
# Add softsailor to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from softsailor.router import Router
from softsailor.sol.sol_functions import get_chart, get_course, get_settings

sts = get_settings()
sts.save_to_file('race.xml')
chrt = get_chart()
crs = get_course()
chrt.save_to_kml('map.kml')
crs.save_to_kml('course.kml')

rtr = Router(chart=chrt, boat=None, course=crs)

for i, route in enumerate(rtr.course_routes):
    route.save_to_kml('route_%d.kml' % i)
    route.save_to_file('route_%d.txt' % i)

