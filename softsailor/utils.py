import os
import math

def get_config_dir():
    script_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.realpath(script_path + '/../etc')
    return config_path

def timedelta_to_seconds(td):
    return td.days * 86400 + td.seconds + td.microseconds * 1E-6

def array_func(func):
    def decorated(*args):
        if len(args) > 1:
            return list(map(func, args))
        else:
            arg = args[0]
            try:
                it = iter(arg)
                return type(arg)(map(func, arg))
            except TypeError:
                return func(arg)
    return decorated

def vec_func(func):
    def decorated(*args):
        if len(args) > 1:
            return func((args[0], args[1]))
        else:
            return func(args[0])
    return decorated

def vec_meth(func):
    def decorated(self, *args):
        if len(args) > 1:
            return func(self, (args[0], args[1]))
        else:
            return func(self, args[0])
    return decorated

@array_func
def deg_to_rad(degs):
    return math.radians(float(degs))

@array_func
def rad_to_deg(value):
    return math.degrees(float(rads))

@array_func
def knots_to_ms(knots):
    return float(knots) * 1852 / 3600

@array_func
def ms_to_knots(ms):
    return ms * 3600 / 1852

@array_func
def str_to_float(value):
    return float(value)

def create_kml_document(name):
    impl = getDOMImplementation()
    dom = impl.createDocument(None, 'kml', None)
    root = dom.documentElement
    root.setAttribute('xmlns', 'http://www.opengis.net/kml/2.2')
    doc = dom.createElement('Document')
    root.appendChild(doc)
    doc_name = dom.createElement('name')
    doc.appendChild(doc_name)
    doc_name_text = dom.createTextNode(name)
    doc_name.appendChild(doc_name_text)
    return (dom, doc)

def save_kml_document(dom, filename):
    f = open(filename, 'w')
    dom.writexml(f, encoding="UTF8")
    f.close()
    dom.unlink()

def normalize_angle_pipi(angle):
    # Normalize angle in -180 <= angle < 180 range
    while angle >= math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi 
    return angle

def normalize_angle_2pi(angle):
    # Normalize angle in 0 <= angle < 360 range
    while angle >= 2 * math.pi:
        angle -= 2 * math.pi
    while angle < 0:
        angle += 2 * math.pi
    return angle

def rectangular_to_polar(vector):
    return (normalize_angle_2pi(math.atan2(vector[1], vector[0])),  \
            math.sqrt(vector[0] * vector[0] + vector[1] * vector[1]))

def polar_to_rectangular(vector):
    return (vector[1] * cos(vector[0]), vector[1] * sin(vector[0]))
