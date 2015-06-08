"""
Sol functions module

Contains functions for interfacing with the sailonline.org
online game status.
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from softsailor.utils import *
from softsailor.world import world

from vr_settings import Settings
from vr_utils import *
from vr_wind import *
from vr_weather import *
from vr_chart import Chart
from vr_course import Course

from datetime import datetime

from geofun import set_earth_model

set_earth_model('spherical')

# Some global singletons required by the functions
__vr_settings_instance = None
__vr_wind_instance = None
__vr_chart_instance = None
__vr_course_instance = None

def get_settings(race_file=None):
    global __vr_settings_instance
    if __vr_settings_instance == None:
        if race_file is None:
            __vr_settings_instance = Settings()
        else:
            __vr_settings_instance = Settings(race_file)
    return __vr_settings_instance

def get_chart():
    global __vr_chart_instance
    if __vr_chart_instance is None:
        __vr_chart_instance = SolChart()
        settings = get_settings()
        if settings.chart != '':
            __vr_chart_instance.load(get_settings().chart)
        else:
            settings = get_settings()
            __vr_chart_instance.load_tiles(
                settings.host,
                settings.tilemap,
                settings.area)
    return __vr_chart_instance

def get_wind():
    global __vr_wind_instance
    if __sol_vr_instance is None:
        weather = Weather()
        weather.load(get_settings())
        __vr_wind_instance = VrWind(weather)
    return __vr_wind_instance

def get_course():
    global __vr_course_instance
    if __vr_course_instance is None:
        settings = get_settings()
        __vr_course_instance = VrCourse(settings.course, 
                                          settings.finish_radius, 
                                          get_chart()) 
    return __vr_course_instance

def fetch_boat(boat):
    """Fetches the online data for boat"""
    settings = get_settings()
    uri = '/webclient/boat.xml?token=' + settings.token
    dom = fetch_sol_document(settings.host, uri)
    root = dom.childNodes[0]
    boat_element = get_element(root, "boat")
    situation = boat.situation
    cog = get_child_float_value(boat_element, "cog")
    situation.position.lat = deg_to_rad(get_child_float_value(boat_element, \
        "lat"))
    situation.position.lon = deg_to_rad(get_child_float_value(boat_element, \
        "lon"))
    # Unfortunately SOL doesn't return a boat time :(
    situation.time = datetime.utcnow()
    sog = kn_to_ms(get_child_float_value(boat_element, "sog"))
    boat.velocity_over_ground = (cog, sog)
    boat.condition.wind = (get_child_float_value(boat_element, "twd"), \
                           get_child_float_value(boat_element, "tws"))
    boat.efficiency = get_child_float_value(boat_element, "efficiency")
    # No currents or drift in sol -> heading = course
    situation.heading = cog
    dom.unlink()

def do_steer(heading):
    """Set heading for online boat"""
    settings = get_settings()
    heading = normalize_angle_2pi(heading)
    post_str = 'command=cc&delay=0&value=' + str(heading)
    uri = '/webclient/command/post/?token=' + settings.token
    conn = HTTPConnection(settings.host)
    conn.request("POST", uri, post_str)
    resp = conn.getresponse()
    data = resp.read()
    data.index('OK')

def do_steer_wind(wind_angle):
    """Set wind angle for online boat"""
    settings = get_settings()
    wind_angle = normalize_angle_pipi(wind_angle)
    post_str = 'command=twa&delay=0&value=' + str(wind_angle)
    uri = '/webclient/command/post/?token=' + settings.token
    conn = HTTPConnection(settings.host)
    conn.request("POST", uri, post_str)
    resp = conn.getresponse()
    data = resp.read()
    data.index('OK')
