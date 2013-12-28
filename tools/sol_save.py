#!/usr/bin/env python2.7

"""
This scripts saves the course and map of the currently configured race to kml
and route txt

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""

import sys, os
import logging

# Add softsailor to the python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from softsailor.utils import setup_log
setup_log('sol_save', logging.DEBUG)
from softsailor.router import Router
from softsailor.sol.sol_functions import get_chart, get_course, get_settings

log = logging.getLogger('tools.sol_save')
log.info('Getting race settings')
sts = get_settings()
sts.save_to_file('race.xml')
log.info('Getting chart')
chrt = get_chart()
chrt.save_to_kml('map.kml')
log.info('Getting race course')
crs = get_course()
crs.save_to_kml('course.kml')

log.info('Setting up router')
rtr = Router(chart=chrt, boat=None, course=crs)
log.info('Constructing race legs')
rtr.construct_legs()

for i, route in enumerate(rtr.course_routes):
    log.info('Saving route %d' % i)
    route.save_to_kml('route_%d.kml' % i)
    route.save_to_file('route_%d.txt' % i)
