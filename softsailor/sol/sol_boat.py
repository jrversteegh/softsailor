from softsailor.boat import SailBoat
from sol_performance import Performance
from sol_settings import *
from sol_functions import get_settings

class Boat(SailBoat):
    def __init__(self, *args, **kwargs):
        super(Boat, self).__init__(*args, **kwargs)
        self.performance = Performance(get_settings().polar_data)
