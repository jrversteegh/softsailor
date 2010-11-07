"""
This module contains functions for interfacing with the sailonline.org
online game status.

Author: Jaap Versteegh <j.r.versteegh@gmail.com>
"""
from softsailor.utils import *

from sol_settings import Settings
from sol_xmlutil import *
from sol_wind import *
from sol_weather import *

# Some global singletons required by the functions
__sol_settings_instance = Settings()
__sol_weather_instance = Weather()
__sol_weather_instance.load(__sol_settings_instance)
__sol_wind_instance = Wind(__sol_weather_instance)

def get_boat(boat):
    """Fetches the online data for boat"""
    settings = __sol_settings_instance
    uri = '/webclient/boat.xml?token=' + settings.token
    dom = fetch_sol_document(settings.host, uri)
    root = dom.childNodes[0]
    boat_element = get_element(root, "boat")
    situation = boat.situation
    cog = get_child_float_value(boat_element, "cog")
    situation.position[0] = deg_to_rad(get_child_float_value(boat_element, \
        "lat"))
    situation.position[1] = deg_to_rad(get_child_float_value(boat_element, \
        "lon"))
    sog = knots_to_ms(get_child_float_value(boat_element, "sog"))
    boat.velocity_over_ground = (cog, sog)
    boat.condition.wind = (get_child_float_value(boat_element, "twd"), \
                           get_child_float_value(boat_element, "tws"))
    boat.efficiency = get_child_float_value(boat_element, "efficiency")
    # No currents or drift in sol -> heading = course
    situation.heading = cog
    dom.unlink()

def get_wind(position, time):
    """Fetch locally interpolated value of online wind at position and time"""
    return __sol_wind_instance.get(position, time)

def do_steer(heading):
    """Set heading for online boat"""
    settings = __sol_settings_instance
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
    settings = __sol_settings_instance
    wind_angle = normalize_angle_pipi(wind_angle)
    post_str = 'command=twa&delay=0&value=' + str(wind_angle)
    uri = '/webclient/command/post/?token=' + settings.token
    conn = HTTPConnection(settings.host)
    conn.request("POST", uri, post_str)
    resp = conn.getresponse()
    data = resp.read()
    data.index('OK')
