"""
Sol updater module

Contains object that update other objects, in particular a boat updater 
implementation for sailonline.org
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from softsailor.updater import BoatUpdater, SimUpdater
from sol_functions import fetch_boat

from datetime import timedelta

class Updater(BoatUpdater):
    def update(self):
        fetch_boat(self.boat)
        super(Updater, self).update()

class SimUpdater(SimUpdater):
    """
    Simulation updater that implements approximation of SOL
    performance penalty by fast forwarding the boat clock
    """
    prev_wind_angle = None
    penalty_multiplier = 1.0
    def update(self):
        super(SimUpdater, self).update()
        wind_angle = self.boat.wind_angle
        if self.prev_wind_angle is not None:
            penalty = abs(wind_angle - self.prev_wind_angle) 
            if penalty > 0.1:
                if (wind_angle * self.prev_wind_angle) < 0:
                    # Tacked or gybed
                    penalty += 1.5 
                penalty *= self.penalty_multiplier * self.boat.speed
                self.boat.time += timedelta(seconds=round(penalty))
        self.prev_wind_angle = wind_angle
