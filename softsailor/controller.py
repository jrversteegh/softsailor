from boat import Boat
from utils import *
from conditions import Condition
from situation import Situation
from motion import Motion

class Controller(object):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        
    def steer_heading(self, heading):
        pass

    def steer_wind_angle(self, wind_angle):
        pass




class BoatController(Controller):
    def __init__(self, *args, **kwargs):
        super(BoatController, self).__init__(*args, **kwargs)
        if len(args) > 0:
            self.boat = args[0]
        else:
            self.boat = kwargs['boat']

    def steer_heading(self, heading):
        self.boat.situation.heading = normalize_angle_2pi(heading)

    def steer_wind_angle(self, wind_angle):
        heading = self.boat.condition.wind[0] - wind_angle 
        self.steer_heading(heading)

