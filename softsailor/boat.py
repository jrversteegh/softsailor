from utils import *
from classes import *
from conditions import *
from performance import *
from motion import *
from situation import *


class Boat(object):
    def __init__(self, *args, **kwargs):
        super(Boat, self).__init__(*args, **kwargs)
        self.situation = Situation()
        self.motion = Motion()
        self.condition = Condition((0, 0), (0, 0))

    @property
    def position(self):
        return self.situation.position
    @position.setter
    def position(self, value):
        self.situation.position = value

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

class Sails(object):
    main_sail = 0
    head_sail = 0
    spinnaker = 0

class SailBoat(Boat):
    def __init__(self, *args, **kwargs):
        super(SailBoat, self).__init__(*args, **kwargs)
        self.sails = Sails()

    @property
    def wind_angle(self):
        return normalize_angle_pipi(self.condition.wind[0] \
            - self.situation.heading)

    @property
    def relative_wind(self):
        return (self.wind_angle, self.condition.wind[1])

    @property
    def apparent_wind(self):
        return PolarVector(self.relative_wind) + PolarVector(0, self.motion.speed)

