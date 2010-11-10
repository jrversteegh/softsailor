"""
This module contains a remoter updater implementation for sailonline.org

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""
from softsailor.updater import BoatUpdater
from sol_functions import fetch_boat

class Updater(BoatUpdater):
    def update(self):
        fetch_boat(self.boat)
        self.log()
