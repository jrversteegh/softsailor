"""
Utils module

Contains utility functions
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import os
import math
import logging
from xml.dom.minidom import parseString, getDOMImplementation
# These are from libkml. You may need to install these
import kmlbase
import kmldom
import kmlengine
from itertools import chain

from geofun import Line, Position, Vector

_output_encoding = 'utf-8'
        
def set_output_encoding(encoding):
    global _output_encoding
    _output_encoding = encoding

def get_config_dir():
    script_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.realpath(script_path + '/../etc')
    return config_path

def timedelta_to_seconds(td):
    return td.days * 86400 + td.seconds + td.microseconds * 1E-6

def encoded(func):
    def decorated(*args, **kwargs):
        if kwargs.has_key('uni'):
            return func(*args)
        else:
            return func(*args).encode(_output_encoding)
    return decorated

def array_func(func):
    """Decorator that creates a function wrapper that accepts multiple 
       arguments or a container for single argument scalar functions
    """
    def decorated(*args):
        if len(args) > 1:
            return list(map(func, args))
        else:
            arg = args[0]
            t = type(arg)
            if t == str or t == unicode:
                return func(arg)
            else:
                try:
                    it = iter(arg)
                    return type(arg)(map(func, arg))
                except TypeError:
                    return func(arg)
    return decorated

def vec_func(func):
    """Decorator that creates a function that accepts a vector as last
       argument, which is exploded before calling the original function"""
    def decorated(*args):
        try:
            it = iter(args[-1])
            args = tuple(chain(args[:-1], it))
        except TypeError:
            pass

        return func(*args)

    return decorated

@array_func
def deg_to_rad(degs):
    return math.radians(float(degs))

@array_func
def rad_to_deg(rads):
    return math.degrees(float(rads))

@array_func
def kn_to_ms(knots):
    return float(knots) * 1852 / 3600

@array_func
def ms_to_kn(ms):
    return ms * 3600 / 1852

@array_func
def m_to_nm(m):
    return m / 1852

@array_func
def nm_to_m(nm):
    return nm * 1852

@array_func
def to_float(value):
    return float(value)

@array_func
def to_string(value):
    return str(value)

@encoded
def tim_to_str(value):
    return value.strftime(time_format)

@encoded
def lat_to_str(value, unsigned=True):
    if value < 0 and unsigned:
        return u"%8.4f \u00B0S" % rad_to_deg(-value)
    else:
        return u"%8.4f \u00B0N" % rad_to_deg(value)

@encoded
def lon_to_str(value, unsigned=True):
    if value < 0 and unsigned:
        return u"%8.4f \u00B0W" % rad_to_deg(-value)
    else:
        return u"%8.4f \u00B0E" % rad_to_deg(value)

@encoded
def pos_to_str(value, unsigned=True):
    return lat_to_str(value[0], unsigned, uni=True) +  u', ' + \
           lon_to_str(value[1], unsigned, uni=True) 

@encoded
def ang_to_str(value):
    return u"%8.2f \u00B0" % rad_to_deg(value)

@encoded
def dst_to_str(value):
    return u"%8.2f nm" % m_to_nm(value)

@encoded
def spd_to_str(value):
    return u"%8.2f kn" % ms_to_kn(value)

@encoded
def vec_to_str(value):
    return ang_to_str(value[0], uni=True) + u', ' + \
           dst_to_str(value[1], uni=True) 

@encoded
def vel_to_str(value):
    return ang_to_str(value[0], uni=True) + u', ' + \
           spd_to_str(value[1], uni=True)

@encoded
def lin_to_str(value):
    return pos_to_str(value[0], uni=True) + ' - ' + \
           pos_to_str(value[2], uni=True)

def add_element_with_text(dom, parent, name, text):
    """Adds an xml element with 'name' and containing 'text' to a existing
       element 'parent'
    """
    element = dom.createElement(name)
    parent.appendChild(element)
    text_node = dom.createTextNode(text)
    element.appendChild(text_node)
    return element

def create_kml_document(name):
    factory = kmldom.KmlFactory_GetFactory()

    icon = factory.CreateIconStyleIcon()
    icon.set_href('http://maps.google.com/mapfiles/kml/paddle/blu-circle.png')

    icon_style = factory.CreateIconStyle()
    icon_style.set_scale(0.64)
    icon_style.set_icon(icon)

    style = factory.CreateStyle()
    style.set_id('default')
    style.set_iconstyle(icon_style)

    icon = factory.CreateIconStyleIcon()
    icon.set_href('http://maps.gstatic.com/intl/en_ALL/mapfiles/' \
                  + 'ms/micons/sailing.white.png')

    icon_style = factory.CreateIconStyle()
    icon_style.set_scale(0.5)
    icon_style.set_icon(icon)

    style_sail = factory.CreateStyle()
    style_sail.set_id('sailboat')
    style_sail.set_iconstyle(icon_style)

    func_line_style = factory.CreateLineStyle()
    func_line_style.set_color(kmlbase.Color32(0xFF66CC66))
    func_line_style.set_width(2)
    func_poly_style = factory.CreatePolyStyle()
    func_poly_style.set_color(kmlbase.Color32(0x9F66CC66))
    style_func = factory.CreateStyle()
    style_func.set_id('func')
    style_func.set_linestyle(func_line_style)
    style_func.set_polystyle(func_poly_style)

    doc = factory.CreateDocument()
    doc.set_name(name)
    doc.add_styleselector(style)
    doc.add_styleselector(style_func)
    doc.add_styleselector(style_sail)

    kml = factory.CreateKml()
    kml.set_feature(doc)
    return (kml, doc)

def create_point_placemark(name, lat, lon):
    factory = kmldom.KmlFactory_GetFactory()

    cs = factory.CreateCoordinates()
    cs.add_latlng(lat, lon)

    pt = factory.CreatePoint()
    pt.set_coordinates(cs)

    pm = factory.CreatePlacemark()
    pm.set_geometry(pt)
    pm.set_name(name)
    return pm

def create_line_placemark(name, coords):
    factory = kmldom.KmlFactory_GetFactory()

    cs = factory.CreateCoordinates()
    for lat, lon in coords:
        cs.add_latlng(lat, lon)

    ls = factory.CreateLineString()
    ls.set_tessellate(True)
    ls.set_coordinates(cs)

    pm = factory.CreatePlacemark()
    pm.set_geometry(ls)
    pm.set_name(name)
    return pm

def create_func_placemark(name, func, scale = 1):
    factory = kmldom.KmlFactory_GetFactory()

    cs = factory.CreateCoordinates()
    for lat, lon, val in func:
        val *= scale
        cs.add_latlngalt(lat, lon, val)

    ls = factory.CreateLineString()
    ls.set_tessellate(True)
    ls.set_extrude(True)
    ls.set_coordinates(cs)
    ls.set_altitudemode(kmldom.ALTITUDEMODE_ABSOLUTE)

    pm = factory.CreatePlacemark()
    pm.set_geometry(ls)
    pm.set_name(name)
    pm.set_styleurl('#func')
    return pm

def save_kml_document(kml, filename):
    f = open(filename, 'w')
    kml_file = kmlengine.KmlFile.CreateFromImport(kml)
    ok, xml = kml_file.SerializeToString()
    f.write(xml)
    f.close()

pi = math.pi
two_pi = 2 * math.pi
half_pi = math.pi / 2
time_format = "%Y-%m-%d %H:%M:%S"

def normalize_angle_pipi(angle):
    # Normalize angle in -180 <= angle < 180 range
    while angle >= math.pi:
        angle -= two_pi
    while angle < -math.pi:
        angle += two_pi
    return angle

def normalize_angle_2pi(angle):
    # Normalize angle in 0 <= angle < 360 range
    while angle >= two_pi:
        angle -= two_pi
    while angle < 0:
        angle += two_pi
    return angle

def angle_diff(angle1, angle2):
    return normalize_angle_pipi(angle1 - angle2)

def rectangular_to_polar(vector):
    return (normalize_angle_2pi(math.atan2(vector[1], vector[0])),  \
            math.sqrt(vector[0] * vector[0] + vector[1] * vector[1]))

def polar_to_rectangular(vector):
    return (vector[1] * math.cos(vector[0]), vector[1] * math.sin(vector[0]))

def bearing_to_heading(bearing, speed, current):
    result = bearing[0]
    if speed != 0 and current[1] != 0:
        result += math.asin(current[1] * math.sin(bearing[0] + current[0]) / speed)
        normalize_angle_2pi(result)
    return result
        
def push_out(points, offset=42, chart=None):
    if points is None:
        return None
    result = []
    i = iter(points)
    try:
        cur = i.next()
        result.append(Position(cur))
        try:
            nxt = i.next()
            v_from = nxt - cur
            try:
                while True:
                    prv = cur
                    cur = nxt
                    nxt = i.next()
                    v_to = v_from
                    v_from = nxt - cur
                    ad = angle_diff(v_from.a, v_to.a)
                    o = offset
                    if ad > 0:
                        a = normalize_angle_2pi(v_to.a + 0.5 * (ad - pi))
                    elif ad < 0:
                        a = normalize_angle_2pi(v_to.a + 0.5 * (ad + pi))
                    else:
                        a = 0
                        o = 0
                    v = Vector(a, o)
                    p = cur + v
                    if chart is not None:
                        l = Line(cur + v * 0.01, p)
                        segment, intersect = chart.intersect(l)
                        if intersect is not None:
                            p = cur + (intersect - cur) * 0.5

                    result.append(p)
            except StopIteration:
                result.append(Position(nxt))
        except StopIteration:
            pass
    except StopIteration:
        pass
    return result

def veer_vector(vec, right, distance=42):
    result = Vector(vec)
    result.r = distance
    if right:
        result.a += 0.5 * pi
    else:
        result.a -= 0.5 * pi
    return result


def setup_log(logname, level=logging.INFO):
    try:
        os.remove(logname)
    except:
        pass
    logging.basicConfig(filename=logname + '.log', 
                        level=level,
                        filemode='w', 
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
