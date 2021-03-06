"""
Motion module

Contains an object that contains the dynamic state of an object
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from geofun import Vector

class Motion(object):
    speed = 0
    course = 0

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            course = args[0]
            speed = args[1]
        elif len(args) > 0:
            course = args[0][0]
            speed = args[0][1]

    @property
    def velocity(self):
        return Vector(self.course, self.speed) 
    @velocity.setter
    def velocity(self, value):
        self.course = value[0]
        self.speed = value[1]
