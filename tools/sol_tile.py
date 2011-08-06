#!/usr/bin/env python2.7

"""
This scripts saves the course and map of the currently configured race to kml

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""

import sys, os
# Add softsailor to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import zlib
import urllib

tiles = 'h'
lon_i = 204
lat_i = 148

stream = urllib.urlopen(
    'http://race.sailport.se/site_media/maps/tiles/%s/%d_%d.xml.z' \
    % (tiles, lon_i, lat_i))
data = zlib.decompress(stream.read())
f = open('%d_%d.xml' % (lon_i, lat_i), 'w')
f.write(data)
f.close()
