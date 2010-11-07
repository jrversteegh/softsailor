"""
This module contains a remoter updater implementation for sailonline.org

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""
from softsailor.updater import BoatUpdater
from sol_functions import get_boat

class SolUpdater(BoatUpdater):
    def update(self):
        get_boat(self.boat)
