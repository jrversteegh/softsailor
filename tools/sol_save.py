#!/usr/bin/env python

"""
This scripts saves the course and map of the currently configured race to kml

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""

import sys, os
# Add softsailor to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from softsailor.sol.sol_functions import get_map, get_course

map = get_map()
crs = get_course()

map.save_to_kml('map.kml')
crs.save_to_kml('course.kml')
