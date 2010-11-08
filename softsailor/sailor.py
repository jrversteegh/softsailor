from utils import *
class Sailor(object):
    """Handles sailing a boat along a route"""
    def __init__(self, *args, **kwargs):
        super(Sailor, self).__init__()
        if len(args) > 0:
            self.boat = args[0]
            self.controller = args[1]
            self.updater = args[2]
            self.router = args[3]
            self.map = args[4]
        else:
            self.boat = kwargs['boat']
            self.controller = kwargs['controller']
            self.updater = kwargs['updater']
            self.router = kwargs['router']
            self.map = kwargs['map']

    def sail(self):
        self.updater.update()
        new_heading = self.get_heading()
        if abs(new_heading - self.boat.heading) > 0.1:
            self.controller.do_steer(new_heading)
        
    def get_heading(self):
        bearing, distance = self.router.get_bearing()
        heading = bearing_to_heading(bearing, \
                self.boat.speed, self.boat.conditions.current) 
        heading, wind_angle = self.adjust_heading_for_wind(heading)

    def adjust_heading_for_wind(self, heading):
        wind = self.boat.condition.wind
        wind_angle = normalize_angle_pipi(wind[0] - heading)
        if wind_angle < 0:
            abs_wind_angle = -wind_angle
            sign = -1
        else:
            abs_wind_angle = wind_angle
            sign = 1
        opt_angles = self.boat.performance.get_optimal_angles(wind[1])
        if abs_wind_angle < opt_angles[0]:
            new_wind_angle = opt_angles[0] * sign
        elif abs_wind_angle > opt_angles[1]:
            new_wind_angle = opt_angles[1] * sign
        else:
            return heading, wind_angle
        return normalize_angle_2pi(new_wind_angle + wind[0]), new_wind_angle
