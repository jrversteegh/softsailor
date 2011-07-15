"""
Sol world module

Contains world implementation for sol
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"
from softsailor.world import world
from sol_functions import get_wind, get_map

world.wind = get_wind()
world.map = get_map()


