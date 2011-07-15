"""
Boat module

Contains boat and sailboat objects
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from utils import *
from classes import *
from conditions import *
from performance import *
from motion import *
from situation import *


class Boat(object):
    def __init__(self, *args, **kwargs):
        super(Boat, self).__init__()
        self.situation = Situation()
        self.motion = Motion()
        self.condition = Condition((0, 0), (0, 0))
        for key in kwargs:
            if key == 'position':
                self.position = kwargs[key]

    @property 
    def time(self):
        return self.situation.time
    @time.setter
    def time(self, value):
        self.situation.time = value

    @property
    def position(self):
        return self.situation.position
    @position.setter
    def position(self, value):
        self.situation.position = Position(value)

    @property
    def heading(self):
        return self.situation.heading
    @heading.setter
    def heading(self, value):
        self.situation.heading = value

    @property
    def speed(self):
        return self.motion.speed
    @speed.setter
    def speed(self, value):
        self.motion.speed = value

    @property
    def velocity_over_ground(self):
        return PolarVector(self.motion.velocity) \
                + PolarVector(self.condition.current)
    @velocity_over_ground.setter
    def velocity_over_ground(self, value):
        self.motion.velocity = PolarVector(value) \
                - PolarVector(self.condition.current)

    @property 
    def drift(self):
        return normalize_angle_pipi(self.motion.course - self.heading)
    @drift.setter
    def drift(self, value):
        self.motion.course = normalize_angle_2pi(self.heading + value)

class Sails(object):
    main_sail = 0
    head_sail = 0
    spinnaker = 0

class SailBoat(Boat):
    def __init__(self, *args, **kwargs):
        super(SailBoat, self).__init__(*args, **kwargs)
        self.sails = Sails()
        self.performance = Performance()

    @property
    def wind_angle(self):
        return normalize_angle_pipi(self.condition.wind[0] \
            - self.heading)

    @property
    def relative_wind(self):
        return (self.wind_angle, self.condition.wind[1])

    @property
    def apparent_wind(self):
        return PolarVector(self.relative_wind) + PolarVector(0, self.motion.speed)

