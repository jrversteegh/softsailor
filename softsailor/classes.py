import math
import numpy as np

from utils import *

def dxy_dpos(latitude, longitude):
    """Simple earth model"""
    return 6367311.8, 6378134.3 * math.cos(latitude)

class Vector(object):
    @property
    def ar(self):
        return self.a, self.r

    @ar.setter
    def ar(self, value):
        self.a, self.r = value

    @property
    def xy(self):
        return self.x, self.y

    @xy.setter
    def xy(self, value):
        self.x, self.y = value

    def __getitem__(self, index):
        if index == 0:
            return self.a
        elif index == 1:
            return self.r
        else:
            raise IndexError("Vector index should be 0 or 1")

    def __setitem__(self, index, value):
        if index == 0:
            self.a = value
        elif index == 1:
            self.r = value
        else:
            raise IndexError("Vector index should be 0 or 1")

    def __iter__(self):
        return iter((self.a, self.r))

    def __iadd__(self, vector):
        self.x += vector.x
        self.y += vector.y
        return self

    def __isub__(self, vector):
        self.x -= vector.x
        self.y -= vector.y
        return self

    def __imul__(self, scalar):
        self.r *= scalar
        return self

    def __add__(self, vector):
        result = PolarVector(vector)
        result.x = result.x + self.x
        result.y = result.y + self.y
        return result

    def __sub__(self, vector):
        result = CartesianVector(self.xy)
        result.x -= vector.x
        result.y -= vector.y
        return result

    def __mul__(self, scalar):
        result = PolarVector(self)
        result.r *= scalar
        return result

    def __str__(self):
        return '(' + str(rad_to_deg(self.a)) + ', ' + str(self.r) + ')-(' + str(self.x) + \
                ', ' + str(self.y) + ')'

    def dot(self, vector):
        return self.x * vector.x + self.y * vector.y

    def cross(self, vector):
        return self.x * vector.y - self.y * vector.x 

    def equals(self, vector):
        return np.allclose(self.a, vector[0]) and np.allclose(self.r, vector[1])
    

class PolarVector(Vector):
    def __init__(self, a_or_vector, r = None):
        if r == None:
            self.a, self.r = a_or_vector
        else:
            self.a = a_or_vector
            self.r = r

    @property
    def x(self):
        return self.r * math.cos(self.a)

    @x.setter
    def x(self, value):
        y = self.y
        self.a = math.atan2(y, value)
        self.r = math.sqrt(value * value + y * y)

    @property
    def y(self):
        return self.r * math.sin(self.a)

    @y.setter
    def y(self, value):
        x = self.x
        self.a = math.atan2(value, x)
        self.r = math.sqrt(x * x + value * value)

    # Performance property setter overload
    @Vector.xy.setter
    def xy(self, value):
        self.x = math.atan2(value[1], value[0])
        self.y = math.sqrt(value[0] * value[0] + value[1] * value[1])

class CartesianVector(Vector):
    def __init__(self, x_or_vector, y = None):
        if y == None:
            self.x, self.y = x_or_vector
        else:
            self.x = x_or_vector
            self.y = y

    @property
    def a(self):
        return math.atan2(self.y, self.x)

    @a.setter
    def a(self, value):
        r = self.r
        self.x = r * math.cos(value)
        self.y = r * math.sin(value)

    @property
    def r(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    @r.setter
    def r(self, value):
        a = self.a
        self.x = value * math.cos(a)
        self.y = value * math.sin(a)

    # Performance property setter overload
    @Vector.ar.setter
    def ar(self, value):
        self.x = value[1] * cos(value[0])
        self.y = value[1] * sin(value[0])

class Position(object):
    def __init__(self, latitude_or_vector, longitude = None):
        if longitude == None:
            self.latitude = latitude_or_vector[0]
            self.longitude = latitude_or_vector[1]
        else:
            self.latitude = latitude_or_vector
            self.longitude = longitude
        # Initialize earth model
        self.dxy_dpos = dxy_dpos

    @property
    def dxy(self):
        return self.dxy_dpos(self.latitude, self.longitude) 

    @vec_meth
    def bearing(self, position):
        dxy1 = self.dxy
        dxy2 = self.dxy_dpos(*position)
        dx = 0.5 * (dxy1[0] + dxy2[0])
        dy = 0.5 * (dxy1[1] + dxy2[1])
        x = dx * (self.latitude - position[0])
        y = dy * (self.longitude - position[1])
        return CartesianVector(x, y)

    def __getitem__(self, index):
        if index == 0:
            return self.latitude
        elif index == 1:
            return self.longitude
        else:
            raise IndexError("Position index should be 0 or 1")

    def __setitem__(self, index, value):
        if index == 0:
            self.latitude = value
        elif index == 1:
            self.longitude = value
        else:
            raise IndexError("Position index should be 0 or 1")

    def __iadd__(self, vector):
        dxy = self.dxy
        self.latitude += vector.x / dxy[0]
        self.longitude += vector.y / dxy[1]
        return self

    def __isub__(self, vector):
        dxy = self.dxy
        self.latitude -= vector.x / dxy[0]
        self.longitude -= vector.y / dxy[1]
        return self

    def __add__(self, vector):
        result = Position(self)
        result += vector
        return result

    def __sub__(self, vector_or_position):
        if isinstance(vector_or_position, Position):
            result = self.bearing(vector_or_position)
        else:
            result = Position(self)
            result -= vector_or_position
        return result

    def __str__(self):
        return '(' + str(rad_to_deg(self.latitude)) + ', ' + \
                         str(rad_to_deg(self.longitude)) + ')'


class PolarData:
    speeds = []
    angles = []
    data = []

