"""
Sol settings module

Contains settings for sailonline interfacing
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import logging
_log = logging.getLogger('softsailor.sol.sol_settings')
from ConfigParser import ConfigParser

from softsailor.utils import *
from softsailor.polars import Polars

from sol_xmlutil import *
from geofun import Position

class SettingsNotFound(Exception):
    pass

class Settings:
    token = ''
    host = ''
    race = 0
    race_uri = ''
    boat = ''
    weather = ''
    chart = ''
    def __init__(self, *args):
        _log.debug('Constructing settings')
        if len(args) > 0:
            self.load_race(args[0])
            # Set the default host for loading maps and weather
            self.host = 'race.sailport.se'
        else:
            self.load_file()
            self.load_race()

    def load_file(self):
        config = ConfigParser()
        config_file = get_config_dir() + '/solconfig'
        _log.info('Reading settings from: %s' % config_file)
        files_read = config.read(config_file)
        if len(files_read) < 1:
            raise SettingsNotFound(config_file)
        
        self.host = config.get('SOL', 'host')
        self.token = config.get('SOL', 'token')
        self.race = config.get('SOL', 'race')
        self.race_uri = '/webclient/auth_raceinfo_' + str(self.race) + '.xml'
        
    def load_race(self, uri=None):
        if uri is None:
            uri = self.race_uri + '?token=' + self.token
            _log.info('Load race from: %s on %s' % (str(uri), self.host))
            self.dom = fetch_sol_document(self.host, uri)
        else:
            _log.info('Load race from: %s' % str(uri))
            self.dom = fetch_sol_document_from_url(uri)
        root = self.dom.childNodes[0]
        self.boat = get_child_text_value(root, 'boaturl')
        if self.boat == '':
            raise Exception('Failed to find boat location')
        self.weather = get_child_text_value(root, 'weatherurl')
        if self.weather == '':
            raise Exception('Failed to find weather location')
        self.tilemap = get_child_text_value(root, 'tilemap')
        self.chart = get_child_text_value(root, 'mapurl')
        if self.chart == '' and self.tilemap == '':
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
        self.load_polars(get_element(root, 'vpp'))
        self.load_course(get_element(root, 'course'))
        self.opponents_url = 'http://' + self.host + \
            get_child_text_value(root, 'url') + '?token=' + self.token
        self.traces_url = 'http://' + self.host + \
            get_child_text_value(root, 'traceUrl') + '?token=' + self.token

    def load_course(self, course):
        self.course = []
        waypoints = get_elements(course, 'waypoint')
        for waypoint in waypoints:
            lat = deg_to_rad(float(get_child_text_value(waypoint, 'lat')))
            lon = deg_to_rad(float(get_child_text_value(waypoint, 'lon')))
            self.course.append(Position(lat, lon))
        self.finish_radius = nm_to_m(float(get_child_text_value(course, 'goal_radius')))
        

    def load_polars(self, vpp):
        speeds = get_child_text_value(vpp, "tws_splined")
        angles = get_child_text_value(vpp, "twa_splined")
        boat_speeds = get_child_text_value(vpp, "bs_splined")

        wss = list(to_float(speeds.split()))
        was = list(deg_to_rad(angles.split()))
        vs = [kn_to_ms(bs.split()) for bs in boat_speeds.split(';') if bs]
        
        self.polars = Polars(wss=wss, was=was, vs=vs)
        '''
        for boat_speeds in boat_speeds_per_angle:
            if boat_speeds.strip() != '':
                self.polars.data.append( \
                        list(kn_to_ms(boat_speeds.split(' '))))
                '''

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.dom.toxml('utf-8'))
 



