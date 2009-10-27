# /webclient/auth_raceinfo_164.xml?token=
# /site_media/maps/xmlmaps/Canary_Brazil.xml?token=
# /webclient/boat.xml?token=
# /webclient/race_164.xml?token=
# /webclient/weatherinfo_57.xml?token=
# /webclient/traces_164.xml?token=


from softsailor.utils import *
from settings import Settings
from xmlutil import *
from wind import *
from weather import *

# Some global singletons required by the functions
__sol_settings_instance = Settings()
__sol_weather_instance = Weather()
__sol_weather_instance.load(__sol_settings_instance)
__sol_wind_instance = Wind(__sol_weather_instance)

def get_boat(boat):
    settings = __sol_settings_instance
    uri = '/webclient/boat.xml?token=' + settings.token
    dom = fetch_sol_document(settings.host, uri)
    root = dom.childNodes[0]
    boat_element = get_element(root, "boat")
    boat.course = get_child_float_value(boat_element, "cog")
    # No currents in sol
    boat.heading = boat.course
    boat.position[0] = deg_to_rad(get_child_float_value(boat_element, "lat"))
    boat.position[1] = deg_to_rad(get_child_float_value(boat_element, "lon"))
    boat.speed = knots_to_ms(get_child_float_value(boat_element, "sog"))
    boat.wind = (get_child_float_value(boat_element, "twd"), \
                 get_child_float_value(boat_element, "tws"))
    dom.unlink()

def get_wind(position, time):
    return __sol_wind_instance.get(position, time)

def do_steer(heading):
    settings = __sol_settings_instance
    post_str = 'command=cc&delay=0&value=' + str(heading)
    uri = '/webclient/command/post/?token=' + settings.token
    conn = HTTPConnection(settings.host)
    conn.request("POST", uri, post_str)
    resp = conn.getresponse()
    data = resp.read()
    data.index('OK')

