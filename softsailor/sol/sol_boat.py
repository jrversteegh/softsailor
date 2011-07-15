"""
Sol boat module

Contains a boat with sol performance
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from softsailor.boat import SailBoat
from sol_performance import Performance
from sol_settings import *
from sol_functions import get_settings

class Boat(SailBoat):
    def __init__(self, *args, **kwargs):
        super(Boat, self).__init__(*args, **kwargs)
        self.performance = Performance(get_settings().polar_data)
