import testing_helper

from geofun import Position

from softsailor.utils import *


def gen_waypoints():
    result = []
    # Rotterdam start
    result.append(Position(deg_to_rad(52.00), deg_to_rad( 4.10)))
    # Somewhere on the english coast a little north of newcastle
    result.append(Position(deg_to_rad(55.64), deg_to_rad(-1.55)))
    # Skagen
    result.append(Position(deg_to_rad(57.74), deg_to_rad(10.60)))
    # South of laeso island
    result.append(Position(deg_to_rad(57.20), deg_to_rad(11.15)))
    # Goteborg finish
    result.append(Position(deg_to_rad(57.61), deg_to_rad(11.70)))
    return result

def gen_waypoints_pb3_2011():
    """Race along the shores of estonia"""
    # Good race for collision detection
    result = []
    result.append(Position(*deg_to_rad(58.3700, 24.5000)))
    result.append(Position(*deg_to_rad(58.9036, 23.3503)))
    result.append(Position(*deg_to_rad(58.9500, 23.5000)))
    result.append(Position(*deg_to_rad(59.2200, 23.5200)))
    result.append(Position(*deg_to_rad(59.4870, 24.7080)))
    result.append(Position(*deg_to_rad(59.4690, 24.8190)))
    return result
