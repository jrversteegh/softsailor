import os
import math

def get_config_dir():
    script_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.realpath(script_path + '/../etc')
    return config_path

def timedelta_to_seconds(td):
    return td.days * 86400 + td.seconds + td.microseconds / 1E6

def deg_to_rad(degs):
    try:
        return math.pi * float(degs) / 180
    except TypeError:
        it = iter(degs)
        result = []
        for value in it:
            result.append(math.pi * float(value) / 180)
        return result

def rad_to_deg(rads):
    return 180 * rads / math.pi

def knots_to_ms(knots):
    try:
        return float(knots) * 1852 / 3600
    except TypeError:
        it = iter(knots)
        result = []
        for value in it:
            if value != '':
                result.append(float(value) * 1852 / 3600)
        return result

def str_to_float(value):
    try:
        return float(value)
    except TypeError:
        it = iter(value)
        result = []
        for val in it:
            if val != '':
                result.append(float(val))
        return result

def ms_to_knots(ms):
    return ms * 3600 / 1852

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
