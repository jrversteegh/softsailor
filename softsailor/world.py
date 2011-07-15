"""
World module

Contains and intergration of wind, current and map data
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from softsailor.wind import Wind
from softsailor.current import Current
from softsailor.map import Map

class World(object):
    wind = Wind()
    current = Current()
    land = Map()

world = World()
