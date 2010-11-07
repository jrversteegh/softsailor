from classes import Position
from datetime import datetime

class Situation(object):
    __position = Position([0, 0])
    heading = 0
    time = datetime.now()
    
    @property 
    def position(self):
        return self.__position
    @position.setter
    def position(self, value):
        self.__position = Position(value)

