"""
Update module

Contains objects that update other object based on internal or external
information
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from boat import Boat
from classes import *
from utils import *
from world import world
from datetime import datetime, timedelta

class Updater(Logable):
    """Base class for objects that update information"""
    def __init__(self, *args, **kwargs):
        super(Updater, self).__init__()

    def update(self):
        """Update the object"""
        pass

    def record(self):
        """Record status of object"""
        pass

class BoatUpdater(Updater):
    """Base class for objects that update boat information"""
    def __init__(self, *args, **kwargs):
        super(BoatUpdater, self).__init__(*args, **kwargs)
        if len(args) > 0:
            self.boat = args[0]
        else:
            self.boat = kwargs['boat']
        self.fmtrs = [
            tim_to_str,
            lat_to_str,
            lon_to_str,
            ang_to_str,
            spd_to_str,
            ang_to_str,
            spd_to_str]

    def record(self):
        self.log('log',
                 self.boat.time, 
                 self.boat.position[0],
                 self.boat.position[1], 
                 self.boat.heading, 
                 self.boat.speed, 
                 self.boat.condition.wind[0], 
                 self.boat.condition.wind[1])

    def update(self):
        super(BoatUpdater, self).update()
        self.record()

    def save_to_kml(self, filename):
        kml, doc = create_kml_document(filename)
        factory = kmldom.KmlFactory_GetFactory()
        func = []
        for record in self.records:
            fields = record[2] 
            # function point has format lat,lon,value (speed here)
            lat, lon = rad_to_deg(fields[1], fields[2])
            func.append((lat, lon, ms_to_kn(fields[4])))
        track = create_func_placemark('Track', func, 3600 / 18.52)
        doc.add_feature(track)

        for i, record in enumerate(self.records[::60]):
            fields = record[2] 
            lat, lon = rad_to_deg(fields[1], fields[2])
            pm = create_point_placemark(str(i), lat, lon)
            pm.set_styleurl('#sailboat')
            ts = factory.CreateTimeStamp()
            ts.set_when(fields[0].isoformat())
            pm.set_timeprimitive(ts)
            descr = 'Time: ' + tim_to_str(fields[0]) + "\n" \
                  + 'Heading: ' + ang_to_str(fields[3]) + "\n" \
                  + 'Speed: ' + spd_to_str(fields[4]) + "\n" \
                  + 'Wind dir: ' + ang_to_str(fields[5]) + "\n" \
                  + 'Wind spd: ' + spd_to_str(fields[6])  
        
            pm.set_description(descr)
            doc.add_feature(pm)

        save_kml_document(kml, filename)

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
    """Class that updates boat using simulated time and predicted conditions"""
    timestep = timedelta(seconds=15)

    def update(self):
        boat = self.boat
        boat.condition.wind = world.wind.get(boat.position, boat.time)
        boat.condition.current = world.current.get(boat.position, boat.time)
        performance = boat.performance.get( \
                (boat.wind_angle, boat.condition.wind[1]))
        boat.speed = performance[1]
        boat.motion.course = normalize_angle_2pi( \
                boat.heading - math.copysign(performance[0], boat.wind_angle))

        vog = boat.motion.velocity + boat.condition.current
        boat.position += vog * self.timestep.total_seconds()
        boat.time += self.timestep
        super(SimUpdater, self).update()


