"""
This module contains a remoter controller implementation for sailonline.org

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""
from softsailor.controller import BoatController
from sol_functions import do_steer, do_steer_wind

class SolController(BoatController):
    def steer_heading(self, value):
        do_steer(value)

    def stop(self):
        do_steer_wind(0)
