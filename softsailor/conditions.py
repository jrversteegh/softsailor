from classes import *
from datetime import datetime

class Condition(object):
    __wind = PolarVector(0, 0)
    __current = PolarVector(0, 0)
    def __init__(self, *args, **kwargs):
        super(Condition, self).__init__()
        if len(args) > 0:
            self.wind = args[0]
            if len(args) > 1:
                self.current = args[1]
            else:
                self.current = kwargs['current']
        else:
            self.wind = kwargs['wind']

    @property
    def wind(self):
        return self.__wind
    @wind.setter
    def wind(self, value):
        self.__wind = PolarVector(value)

    @property
    def current(self):
        return self.__current
    @current.setter
    def current(self, value):
        self.__current = PolarVector(value)

class Conditions(object):
    def get_wind(self, lat, lon, time = None):
        return (0, 0)

    def get_current(self, lat, lon, time = None):
        return (0, 0)

    def get_condition(self, lat, lon, time = None):
        if time == None:
            time = datetime.utcnow()
        return Condition(self.get_wind(lat, lon, time), \
                         self.get_current(lat, lon, time))
        

