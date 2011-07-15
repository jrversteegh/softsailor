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
        dom = fetch_sol_document(self.host, uri)
        root = dom.childNodes[0]
        self.boat = get_child_text_value(root, 'boaturl')
        self.weather = get_child_text_value(root, 'weatherurl')
        self.map = get_child_text_value(root, 'mapurl')
        self.load_polars(get_element(root, 'vpp'))

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
 



