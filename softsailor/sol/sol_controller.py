"""
This module contains a remoter controller implementation for sailonline.org

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""
import time
from softsailor.utils import *
from softsailor.controller import BoatController
from softsailor.boat import SailBoat
from sol_functions import do_steer, do_steer_wind, fetch_boat

class Controller(BoatController):
    wait_interval = 2
    wait_retry = 20 # Should be multiple of wait_interval
    wait_timeout = 40
    def steer_heading(self, value):
        boat = self.boat
        # When tacking, stop the boat first. This can lead to performance gain
        wind_angle = normalize_angle_pipi(boat.condition.wind[0] - value)
        if abs(wind_angle) < 1.5 and (wind_angle * boat.wind_angle) < 0:
            self.stop()
        do_steer(value)
        secs = 0
        while abs(boat.heading - value) > 0.001:
            fetch_boat(boat)
            time.sleep(self.wait_interval)
            secs += self.wait_interval
            if secs == self.wait_retry:
                do_steer(value)
            if secs > self.wait_timeout:
                raise ControllerError("Failed to steer SOL boat")

    def stop(self):
        do_steer_wind(0)
        secs = 0
        while (self.boat.speed > 0.001) or (self.boat.efficiency < 0.999):
            fetch_boat(self.boat)
            time.sleep(self.wait_interval)
            secs += self.wait_interval
            if secs == self.wait_retry:
                do_steer_wind(0)
            if secs > self.wait_timeout:
                raise ControllerError("Failed to stop SOL boat")
