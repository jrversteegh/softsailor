"""
Sol settings module

Contains settings for sailonline interfacing
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from ConfigParser import ConfigParser

from softsailor.utils import *
from softsailor.classes import PolarData

from sol_xmlutil import *
from geofun import Position

class SettingsNotFound(Exception):
    pass

class Settings:
    token = ''
    host = ''
    race = 0
    race_url = ''
    boat = ''
    weather = ''
    map = ''
    def __init__(self):
        self.polar_data = PolarData()
        self.load_file()
        self.load_race()

    def load_file(self):
        config = ConfigParser()
        config_file = get_config_dir() + '/solconfig'
        files_read = config.read(config_file)
        if len(files_read) < 1:
            raise SettingsNotFound(config_file)
        
        self.host = config.get('SOL', 'host')
        self.token = config.get('SOL', 'token')
        self.race = config.get('SOL', 'race')
        self.race_url = '/webclient/auth_raceinfo_' + str(self.race) + '.xml'
        
    def load_race(self):
        uri = self.race_url + '?token=' + self.token
        self.dom = fetch_sol_document(self.host, uri)
        #print dom.toxml("utf-8")
        root = self.dom.childNodes[0]
        self.boat = get_child_text_value(root, 'boaturl')
        if self.boat == '':
            raise Exception('Failed to find boat location')
        self.weather = get_child_text_value(root, 'weatherurl')
        if self.weather == '':
            raise Exception('Failed to find weather location')
        self.tilemap = get_child_text_value(root, 'tilemap')
        self.map = get_child_text_value(root, 'mapurl')
        if self.map == '' and self.tilemap == '':
            raise Exception('Failed to find map location')
        self.area = [-half_pi, half_pi, -pi, pi]
        minlat = get_child_text_value(root, 'minlat')
        if minlat != '':
            maxlat = get_child_text_value(root, 'maxlat')
            minlon = get_child_text_value(root, 'minlon')
            maxlon = get_child_text_value(root, 'maxlon')
            self.area[0] = deg_to_rad(float(minlat))
            self.area[1] = deg_to_rad(float(maxlat))
            self.area[2] = deg_to_rad(float(minlon))
            self.area[3] = deg_to_rad(float(maxlon))
        self.opponents = 'http://' + self.host + \
            get_child_text_value(root, 'url') + '?token=' + self.token
        self.traces = 'http://' + self.host + \
            get_child_text_value(root, 'traceUrl') + '?token=' + self.token
        self.load_polars(get_element(root, 'vpp'))
        self.load_course(get_element(root, 'course'))

    def load_course(self, course):
        self.course = []
        waypoints = get_elements(course, 'waypoint')
        for waypoint in waypoints:
            lat = deg_to_rad(float(get_child_text_value(waypoint, 'lat')))
            lon = deg_to_rad(float(get_child_text_value(waypoint, 'lon')))
            self.course.append(Position(lat, lon))
        self.finish_radius = nm_to_m(float(get_child_text_value(course, 'goal_radius')))
        

    def load_polars(self, vpp):
        speed_text = get_child_text_value(vpp, "tws_splined")
        angle_text = get_child_text_value(vpp, "twa_splined")
        boat_speed_text = get_child_text_value(vpp, "bs_splined")

        self.polar_data.speeds = list(to_float(speed_text.split(' ')))
        self.polar_data.angles = list(deg_to_rad(angle_text.split(' ')))
        boat_speeds_per_angle = boat_speed_text.split(';')
        
        self.polar_data.data = []
        for boat_speeds in boat_speeds_per_angle:
            if boat_speeds.strip() != '':
                self.polar_data.data.append( \
                        list(kn_to_ms(boat_speeds.split(' '))))

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.dom.toxml('utf-8'))
 



