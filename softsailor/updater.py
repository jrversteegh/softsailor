from boat import Boat
from classes import *
from utils import *
from world import world
from datetime import datetime, timedelta

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
        pos = boat.position
        wind = boat.condition.wind
        record = (boat.time, pos[0], pos[1], boat.heading, boat.speed, \
                  wind[0], wind[1])
        self.__log.append(record)

    def update(self):
        self.log()

    def save_log(self, filename):
        """Save the stored tracklog to filename in txt and kml format"""
        f = open(filename + '.txt', "w")
        for record in self.__log:
            lat, lon, heading = rad_to_deg(record[1:4])
            record = (record[0].strftime(time_format), \
                      lat, lon, heading, ms_to_knots(record[4]), \
                      rad_to_deg(record[5]), ms_to_knots(record[6]))
            record_str = to_string(record)
            f.write(", ".join(record_str) + "\n")
        f.close()

        kml, doc = create_kml_document(filename)
        factory = kmldom.KmlFactory_GetFactory()
        func = []
        for record in self.__log:
            # function point has format lat,lon,value (speed here)
            lat, lon = rad_to_deg(record[1], record[2])
            func.append((lat, lon, record[4]))
        track = create_func_placemark('Track', func, 3600 / 18.52)
        doc.add_feature(track)

        for i, record in enumerate(self.__log[::60]):
            lat, lon = rad_to_deg(record[1], record[2])
            pm = create_point_placemark(str(i), lat, lon)
            pm.set_styleurl('#sailboat')
            ts = factory.CreateTimeStamp()
            ts.set_when(record[0].isoformat())
            pm.set_timeprimitive(ts)
            descr = u'Heading: ' + u"%.2f\u00B0\n" % rad_to_deg(record[3]) \
                    + u'Speed : ' + u"%.2f kn" % ms_to_knots(record[4]) \
                    + u'Wind direction: ' + u"%.2f\u00B0\n" % rad_to_deg(record[5]) \
                    + u'Wind speed    : ' + u"%.2f kn" % ms_to_knots(record[6])  
        
            pm.set_description(descr.encode('utf-8'))
            doc.add_feature(pm)

        save_kml_document(kml, filename + '.kml')

class AdjustUpdater(BoatUpdater):
    """Class that updates boat information from another boat"""
    timegap = 0
    distance = 0
    speedgap = 0
    headinggap = 0
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

class SimUpdater(BoatUpdater):
    """Class that update boat using simulated time and data"""
    timestep = timedelta(seconds=15)

    def update(self):
        boat = self.boat
        boat.condition.wind = world.wind.get(boat.position, boat.time)
        boat.speed = boat.performance.get( \
                (boat.wind_angle, boat.condition.wind[1]))
        #boat.motion.course 

        super(SimUpdater, self).update()


