"""
VR settings module

Contains settings for virtual regatta interfacing
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2015, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import logging
_log = logging.getLogger('softsailor.vr.vr_settings')
from ConfigParser import ConfigParser

from softsailor.utils import *
from softsailor.polars import Polars

from vr_utils import *
from geofun import Position

class SettingsNotFound(Exception):
    pass

class Settings:
    host = ''
    user = ''
    key = ''
    weather_url = ''
    chart_url = ''
    vpp_url = ''
    sails = {}
    def __init__(self, *args):
        _log.debug('Constructing settings')
        if len(args) > 0:
            self.load_race(args[0])
            # Set the default host for loading maps and weather
        else:
            self.load_file()
            self.load_race()
            self.load_course()
            self.load_polars()


    def load_file(self):
        config = ConfigParser()
        config_file = get_config_dir() + '/vrconfig'
        _log.info('Reading settings from: %s' % config_file)
        files_read = config.read(config_file)
        if len(files_read) < 1:
            raise SettingsNotFound(config_file)
        
        self.host = config.get('VR', 'host')
        self.user = config.get('VR', 'user')
        self.key = config.get('VR', 'key')
        self.service = config.get('VR', 'service')
        
    def load_race(self, uri=None):
        if uri is None:
            uri = self.service + 'GetConfigFlash'
            _log.info('Load race from: %s on %s' % (str(uri), self.host))
            self.dom = fetch_vr_document(self.host, uri)
        else:
            _log.info('Load race from: %s' % str(uri))
            self.dom = fetch_vr_document_from_url(uri)
        root = self.dom.childNodes[0]
        self.wind_url = get_child_text_value(root, 'UrlWinds')
        if self.wind_url == '':
            raise Exception('Failed to find wind url')
        self.chart_url = get_child_text_value(root, 'UrlMaps')
        if self.chart_url == '':
            raise Exception('Failed to find map url')
        self.vpp_url = get_child_text_value(root, 'UrlVPP')
        if self.vpp_url == '':
            raise Exception('Failed to find vpp url')
        self.vpp_coeff = get_child_float_value(root, 'VPPCoeff')
        self.wind_resolution = float(get_child_text_value(root, 'PRECISION_VENTS'))
        self.wind_block_size = int(get_child_text_value(root, 'TAILLE_ZONE_VENTS'))

    def load_course(self):
        uri = self.service + 'GetCourse'
        dom = fetch_vr_document(self.host, uri)
        root = dom.childNodes[0]
        sails = get_element(root, 'sails')
        sails = get_elements(sails, 'sail')
        for sail in sails:
            ident = sail.getAttribute('id')
            name = sail.getAttribute('name')
            self.sails[ident] = name
        parcours = get_element(root, 'parcoursList')
        parcours = get_elements(root, 'parcours')[-1]
        start = get_element(parcours, 'start')
        finish = get_element(parcours, 'stop')
        checkpoints = get_element(parcours, 'checkpoints')
        waypoints = get_elements(checkpoints, 'checkpoint')
        def point_elem_to_position(elem):
            lat = elem.getAttribute('latitude')
            lon = elem.getAttribute('longitude')
            lat = deg_to_rad(float(lat))
            lon = deg_to_rad(float(lon))
            return Position(lat, lon)

        self.start = start.getAttribute('town')
        self.finish = finish.getAttribute('town')
        self.course = []
        self.course.append(point_elem_to_position(start))
        for waypoint in waypoints:
            self.course.append(point_elem_to_position(waypoint))
        self.course.append(point_elem_to_position(finish))
        self.finish_radius = nm_to_m(float(finish.getAttribute('radius')))
        

    def load_polars(self):
        self.polars = {}
        for sn in self.sails.keys():
            polar_file = self.vpp_url + 'vpp_1_%s.csv' % sn
            polar = Polars(filename=polar_file, smoothing=False, degree=1)
            self.polars[sn] = polar

