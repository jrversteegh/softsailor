"""
Sailor module

Contains a sailor object that integrates all available information
and controls the boat based on that
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import sys
import traceback
from utils import *
from classes import *
from controller import ControllerError

from datetime import datetime

class Sailor(object):
    """Handles sailing a boat along a route"""
    __log_data = []

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

    def __log(self, log_string):
        self.__log_data.append((datetime.utcnow(), log_string))

    def save_log(self, filename):
        f = open(filename + '.txt', "w")
        for record in self.__log_data:
            f.write(str(record[0]) + " " + record[1] + "\n")
        f.close()

    def print_log(self):
        for record in self.__log_data[-5:]:
            print str(record[0]) + " " + record[1]

    def sail(self):
        try:
            self.updater.update()
            if self.router.is_complete:
                return False
            new_heading, is_direct = self.get_heading()
            if abs(new_heading - self.boat.heading) > 0.002:
                try: 
                    if is_direct:
                        self.__log("Steering %.2f" % rad_to_deg(new_heading))
                        self.controller.steer_heading(new_heading)
                    else:
                        wind_angle = normalize_angle_pipi( \
                                self.boat.condition.wind[0] - new_heading)
                        self.__log("Steering wind angle %.2f" % rad_to_deg(wind_angle))
                        self.controller.steer_wind_angle(wind_angle)

                except ControllerError:
                    self.__log("Failed to steer boat")
        except:
            self.__log("General failure while sailing")
            self.__log(traceback.format_exc())
                
        return True
        
    def get_heading(self):
        """Returns new heading and whether this heading is aiming straight
           for the waypoint
        """
        bearing = self.router.get_bearing()
        if self.router.is_complete:
            return self.boat.heading, True
        heading = bearing_to_heading(bearing, \
                self.boat.speed, self.boat.condition.current) 
        adjusted_for_wind, heading = self.adjust_heading_for_wind(heading)
        if adjusted_for_wind:
            # These are only required when we're not headed directly for the
            # waypoint
            changed, heading = self.handle_tacking_and_gybing(heading, bearing)
            changed, heading = self.prevent_beaching(heading)
            return heading, False
        else:
            return heading, True

    def adjust_heading_for_wind(self, heading):
        wind = self.boat.condition.wind
        # Check the suggested heading for suboptimal wind angles
        wind_angle = normalize_angle_pipi(wind[0] - heading)
        if wind_angle < 0:
            abs_wind_angle = -wind_angle
            sign = -1
        else:
            abs_wind_angle = wind_angle
            sign = 1
        opt_angles = self.boat.performance.get_optimal_angles(wind[1])
        # Clip the wind angle to the optimal range...
        if abs_wind_angle < opt_angles[0]:
            new_wind_angle = opt_angles[0] * sign
        elif abs_wind_angle > opt_angles[1]:
            new_wind_angle = opt_angles[1] * sign
        else:
            # Heading indicated a sailable course
            return False, heading
        # ...and return a heading resulting from this wind angle
        return True, normalize_angle_2pi(wind[0] - new_wind_angle)

    def handle_tacking_and_gybing(self, heading, bearing):
        wind = self.boat.condition.wind
        wind_angle = normalize_angle_pipi(wind[0] - heading)
        track, waypoint = self.router.get_active_segment()

        if (wind_angle < 0) != (self.boat.wind_angle < 0):
            # A tack or gybe is apparently suggested...
            # ...revert it in order to prevent excessive tacking/gybing
            heading = normalize_angle_2pi(heading + 2 * wind_angle)
            wind_angle = -wind_angle

        # If we're too far off track, we do have to tack/gybe
        # --> Courses parallel to track are favoured by allowing larger cte
        off_track_angle = normalize_angle_pipi(heading - track[0])
        off_track_mult = 10 \
                + 60 * math.pow(math.cos(0.8 * off_track_angle), 2)
        # --> Lane width as square root of distance to waypoint
        allowed_off_track = off_track_mult * math.sqrt(bearing[1])
        cross_track = self.router.get_cross_track()
        is_off_track = abs(cross_track) > allowed_off_track

        # --> Less than 45 degrees approach angle 
        # (required for safely rounding marks)
        cos_approach_angle = math.cos(track[0] - bearing[0]) 
        approach_lt_45 = cos_approach_angle < 0.72

        if is_off_track or approach_lt_45:
            # ... in which case we'll make sure we steer on a
            # converging tack/reach
            off_bearing_angle = normalize_angle_pipi(heading - bearing[0])
            if (cross_track > 0) == (off_bearing_angle > 0):
                # ...or tack/gybe when they don't
                if approach_lt_45:
                    self.__log("Tacked/gybed to assert <45 degree approach")
                else:
                    self.__log("Tacked/gybed to reduce CTE: %.0f m" \
                               % cross_track)
                return True, normalize_angle_2pi(heading + 2 * wind_angle)
    

        # Nothing needed to be done. Return the originally suggested heading
        return False, heading

    def prevent_beaching(self, heading, look_ahead = None):
        if look_ahead == None:
            look_ahead = 250
        # We'll construct a future course line...
        boat_position = self.boat.position
        # ... project it ahead...
        sail_vector = PolarVector(heading, look_ahead)
        future_position = boat_position + sail_vector
        sail_line = (self.boat.position, sail_vector, future_position)
        # Check if the projected line hits land...
        if self.map.hit(sail_line):
            # ... and if so, tack or gybe away from it
            wind = self.boat.condition.wind
            wind_angle = normalize_angle_pipi(wind[0] - heading)
            self.__log("Tacked/gybed to avoid hitting land")
            return True, normalize_angle_2pi(heading + 2 * wind_angle)

        # Also, we want to keep a clear line of sight to the waypoint
        track, waypoint = self.router.get_active_segment()
        bearing = waypoint.get_bearing_from(self.boat.position)
        view_line = (self.boat.position, bearing, waypoint)
        if self.map.hit(view_line):
            # The only way, we could have gotten something in the view
            # line is that we were reaching or tacking away from the
            # track. Tack or gybe now to get back.
            off_bearing_angle = normalize_angle_pipi(heading - bearing[0])
            off_track = self.router.get_cross_track()
            # Check if heading is 'outside' bearing
            if (off_track > 0) == (off_bearing_angle > 0):
                # ...or tack/gybe when they don't
                wind = self.boat.condition.wind
                wind_angle = normalize_angle_pipi(wind[0] - heading)
                self.__log("Tacked/gybed to avoid land getting in line of sight")
                return True, normalize_angle_2pi(heading + 2 * wind_angle)

        # Nothing needed to be done. Return the originally suggested heading
        return False, heading

