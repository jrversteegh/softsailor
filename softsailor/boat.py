from utils import *

class Boat:
    heading = 0
    position = [0, 0]
    course = 0
    speed = 0
    def steer(self, heading):
        self.heading = heading

class SailBoat(Boat):
    main_sail = 0
    head_sail = 0
    spinnaker = 0
    wind = [0, 0]
    @property
    def wind_angle(self):
        return normalize_angle_pipi(self.wind[0] - self.heading)
    @property
    def relative_wind(self):
        return (self.wind_angle, self.wind[1])

