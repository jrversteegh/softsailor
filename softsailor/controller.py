"""
Controller module

Contains interfaces to the operation of a boat
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from boat import Boat
from utils import *
from conditions import Condition
from situation import Situation
from motion import Motion

class ControllerError(Exception):
    pass


class Controller(object):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__()
        
    def steer_heading(self, heading):
        pass

    def steer_wind_angle(self, wind_angle):
        pass

    def stop(self):
        pass

    def set_main_sail(self, main_sail_no):
        pass

    def set_head_sail(self, head_sail_no):
        pass

    def set_spinnaker(self, spinnaker_no):
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
        heading = normalize_angle_2pi(self.boat.condition.wind[0] - wind_angle)
        self.steer_heading(heading)

    def stop(self):
        self.steer_wind_angle(0)
        self.boat.speed = 0

    def set_main_sail(self, main_sail_no):
        self.boat.sails.main_sail = main_sail_no

    def set_head_sail(self, head_sail_no):
        self.boat.sails.head_sail = head_sail_no

    def set_spinnaker(self, spinnaker_no):
        self.boat.sails.spinnaker = spinnaker_no
