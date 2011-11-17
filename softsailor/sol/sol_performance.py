"""
Sol performance module

Contains a boat performance evaluator for sailonline.org boats
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from bisect import bisect
import math

from softsailor.utils import *
from softsailor.classes import PolarData
from scipy import interpolate

class Performance(object):

    """Boat performance evaluator """

    opt_angles = []
    """array of angles with max and min VMG for each windspeed"""

    def __init__(self, *args, **kwargs):
        """
        Keyword arguments:
            polar_data -- 2D array with boat speeds as function of wind angle and
            direction.
        """
        if len(args) > 0:
            self.polar_data = args[0]
        else:
            self.polar_data = kwargs['polar_data']
        self.__calc_spline_coeffs()
        self.__calc_optimal_angles()

    def get(self, relative_wind):
        """Get boat speed for relative_wind
        
        Arguments:
            relative_wind: 2 item array with absolute wind angle relative to
            boat heading and absolute wind speed .
        """
        angles = self.polar_data.angles
        speeds = self.polar_data.speeds
        data = self.polar_data.data
        coeffs = self.spline_coeffs

        angle = abs(relative_wind[0])
        speed = relative_wind[1]
        angle_j = bisect(angles, angle)
        angle_i = angle_j - 1
        while angle_j >= len(angles):
            angle_j -= 1
            angle_i -= 1

        speed_j = bisect(speeds, speed)
        speed_i = speed_j - 1
        while speed_j >= len(speeds):
            speed_j -= 1
            speed_i -= 1

        angle_range = angles[angle_j] - angles[angle_i] 
        angle_frac = (angle - angles[angle_i]) / float(angle_range)

        speed_range = speeds[speed_j] - speeds[speed_i]
        speed_frac0 = 1
        speed_frac1 = (speed - speeds[speed_i]) / float(speed_range)
        speed_frac2 = speed_frac1 * speed_frac1
        speed_frac3 = speed_frac1 * speed_frac2

        speedi = speed_frac0 * coeffs[angle_i][speed_i][0] + \
                speed_frac1 * coeffs[angle_i][speed_i][1] + \
                speed_frac2 * coeffs[angle_i][speed_i][2] + \
                speed_frac3 * coeffs[angle_i][speed_i][3]
        speedj = speed_frac0 * coeffs[angle_j][speed_i][0] + \
                speed_frac1 * coeffs[angle_j][speed_i][1] + \
                speed_frac2 * coeffs[angle_j][speed_i][2] + \
                speed_frac3 * coeffs[angle_j][speed_i][3]

        return 0, speedi * (1 - angle_frac) + speedj * angle_frac

    def get_drift(self, relative_wind):
        return 0

    def get_speed(self, relative_wind):
        return self.get(relative_wind)[1]

    def get_optimal_angles(self, wind_speed):
        """Return wind angles for min and max VMG at wind_speed"""
        opt_angles = [0, 0]
        speeds = self.polar_data.speeds
        speed_i = bisect_left(speeds, wind_speed)
        speed_j = speed_i + 1
        speed_range = speeds[speed_j] - speeds[speed_i]
        speed_frac = (wind_speed - speeds[speed_i]) / speed_range

        opt_angles[0] = self.opt_angles[speed_i][0] * (1 - speed_frac) + \
                self.opt_angles[speed_j][0] * speed_frac
        opt_angles[1] = self.opt_angles[speed_i][1] * (1 - speed_frac) + \
                self.opt_angles[speed_j][1] * speed_frac
        return opt_angles

    def __calc_optimal_angles(self):
        # Determine max and min VMG wind angles for all wind speeds in
        # polar diagram data
        self.opt_angles = []
        for speed in self.polar_data.speeds:
            opt_angles = [0, math.pi]
            opt_vmgs = [0, 0]
            for angle in self.polar_data.angles:
                boat_perf = self.get((angle, speed))
                course_angle = angle + boat_perf[0]
                boat_speed = boat_perf[1]
                vmg_upwind = math.cos(course_angle) * boat_speed
                vmg_downwind = -math.cos(course_angle) * boat_speed
                if vmg_upwind > opt_vmgs[0]:
                    opt_angles[0] = angle
                    opt_vmgs[0] = vmg_upwind 
                if vmg_downwind > opt_vmgs[1]:
                    opt_angles[1] = angle
                    opt_vmgs[1] = vmg_downwind 
            self.opt_angles.append(opt_angles)

    def __calc_spline_coeffs(self):
        # Determine spline coefficients for interpolation of polar diagram data
        self.spline_coeffs = []
        angles = self.polar_data.angles
        speeds = self.polar_data.speeds
        data = self.polar_data.data
        for i, angle in enumerate(angles):
            coeffs_list = []
            speeds_list = list(enumerate(speeds))
            for j, speed in speeds_list[:-1]:
                if j == 0:
                    a0 =  2 * data[i][j] - data[i][j + 1] 
                else:
                    a0 = data[i][j - 1]
                a1 = data[i][j]
                a2 = data[i][j + 1]
                if j + 2 == len(speeds_list):
                    a3 = 2 * data[i][j + 1] - data[i][j]
                else:
                    a3 = data[i][j + 2]
                coeffs = []
                coeffs.append(a1)
                coeffs.append(-0.5 * a0 + 0.5 * a2)
                coeffs.append(a0 - 2.5 * a1 + 2 * a2 - 0.5 * a3)
                coeffs.append(-0.5 * a0 + 1.5 * a1 - 1.5 * a2 + 0.5 * a3)
                coeffs_list.append(coeffs)
            self.spline_coeffs.append(coeffs_list)


