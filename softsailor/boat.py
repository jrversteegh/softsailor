from utils import *
from classes import *
from conditions import *
from performance import *

class Situation(object):
    heading = 0
    position = [0, 0]

class Motion(object):
    speed = 0
    velocity = [0, 0]
    course = 0
    drift = 0

class Boat(object):
    def __init__(self, *args, **kwargs):
        super(Boat, self).__init__(*args, **kwargs)
        self.situation = Situation()
        self.motion = Motion()
        self.condition = Condition((0,0), (0, 0))

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
        return normalize_angle_pipi(self.condition.wind[0] - self.situation.heading)

    @property
    def relative_wind(self):
        return (self.wind_angle, self.condition.wind[1])

