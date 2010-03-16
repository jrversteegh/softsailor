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
    settings = __sol_settings_instance
    uri = '/webclient/boat.xml?token=' + settings.token
    dom = fetch_sol_document(settings.host, uri)
    root = dom.childNodes[0]
    boat_element = get_element(root, "boat")
    situation = boat.situation
    motion = boat.motion
    motion.course = get_child_float_value(boat_element, "cog")
    # No currents or drift in sol
    situation.heading = motion.course
    situation.position[0] = deg_to_rad(get_child_float_value(boat_element, "lat"))
    situation.position[1] = deg_to_rad(get_child_float_value(boat_element, "lon"))
    motion.speed = knots_to_ms(get_child_float_value(boat_element, "sog"))
    boat.condition.wind = (get_child_float_value(boat_element, "twd"), \
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

