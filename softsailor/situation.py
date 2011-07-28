"""
Situation module

Contains an interface for static orientation and position of a boat
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from geofun import Position
from datetime import datetime

class Situation(object):
    __position = Position(0, 0)
    heading = 0
    def __init__(self, *args, **kwargs):
      self.time = datetime.utcnow()
    
    @property 
    def position(self):
        return self.__position
    @position.setter
    def position(self, value):
        self.__position = Position(value[0], value[1])

