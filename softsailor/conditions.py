"""
Conditions module

Contains classes representing environmental aspects at specific location
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from datetime import datetime

from classes import *
from geofun import Vector

class Condition(object):
    __wind = Vector(0, 0)
    __current = Vector(0, 0)
    def __init__(self, *args, **kwargs):
        super(Condition, self).__init__()
        if len(args) > 0:
            wind = args[0]
            if len(args) > 1:
                current = args[1]
            else:
                current = kwargs['current']
        else:
            wind = kwargs['wind']
        self.__wind = Vector(wind[0], wind[1])
        self.__current = Vector(current[0], current[1])

    @property
    def wind(self):
        return self.__wind
    @wind.setter
    def wind(self, value):
        self.__wind = Vector(value[0], value[1])

    @property
    def current(self):
        return self.__current
    @current.setter
    def current(self, value):
        self.__current = Vector(value[0], value[1])

class Conditions(object):
    def get_wind(self, lat, lon, time = None):
        return Vector(0, 0)

    def get_current(self, lat, lon, time = None):
        return Vector(0, 0)

    def get_condition(self, lat, lon, time = None):
        if time == None:
            time = datetime.utcnow()
        return Condition(self.get_wind(lat, lon, time), \
                         self.get_current(lat, lon, time))
        

