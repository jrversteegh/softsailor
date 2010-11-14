from softsailor.wind import Wind
from softsailor.current import Current
from softsailor.map import Map

class World(object):
    wind = Wind()
    current = Current()
    land = Map()

world = World()
