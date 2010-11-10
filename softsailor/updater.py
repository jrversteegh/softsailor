from boat import Boat
from classes import *
from utils import *

class Updater(object):
    """Base class for objects that update information"""
    def __init__(self, *args, **kwargs):
        super(Updater, self).__init__()
        
    def update(self):
        pass

class BoatUpdater(Updater):
    __log = []
    """Base class for objects that update boat information"""
    def __init__(self, *args, **kwargs):
        super(BoatUpdater, self).__init__(*args, **kwargs)
        if len(args) > 0:
            self.boat = args[0]
        else:
            self.boat = kwargs['boat']

    def log(self):
        boat = self.boat
        pos = rad_to_deg(boat.position)
        record = (boat.time, pos[0], pos[1], \
                  rad_to_deg(boat.heading), ms_to_knots(boat.speed))
        self.__log.append(record)

    def save_log(self, filename):
        """Save the stored tracklog to filename in txt and kml format"""
        f = open(filename + '.txt', "w")
        for record in self.__log:
            record_str = to_string(record)
            f.write(", ".join(record_str) + "\n")
        f.close()
        factory, kml = create_kml_document(filename)
        # TODO insert actual kml coding here
        save_kml_document(kml, filename + '.kml')

class AdjustUpdater(BoatUpdater):
    timegap = 0
    distance = 0
    speedgap = 0
    headinggap = 0
    """Class that updates boat information from another boat"""
    def set_source_boat(self, boat):
        self.source_boat = boat

    def update(self):
        self.timegap = self.source_boat.time - self.boat.time
        self.distance = self.source_boat.position - self.boat.position
        self.speedgap = self.source_boat.speed - self.boat.speed
        self.headinggap = self.source_boat.heading - self.boat.heading
        self.boat.time = self.source_boat.time
        self.boat.position = self.source_boat.position
        self.boat.heading = self.source_boat.heading
        self.boat.speed = self.source_boat.speed

