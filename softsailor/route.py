import os
import datetime
from utils import *
from classes import *
import kmlbase
import kmldom
import kmlengine

class Waypoint(Position):
    range = 100  # Default range for waypoint: 100m
    def __init__(self, *args, **kwargs):
        super(Waypoint, self).__init__(*args[:2], **kwargs)
        if len(args) > 2:
            self.range = args[2]
        elif len(args) > 1:
            try:
                it = iter(args[0])
                self.range = args[1]
            except TypeError:
                pass
        self.comment = ""

    def is_reached(self, position):
        """Return whether the waypoint has been reached by object
           with 'position'
        """
        v = self - position
        return (v[1] < self.range)

class Route(object):
    """Object that contains a list of waypoints"""
    def __init__(self, *args, **kwargs):
        super(Route, self).__init__()
        self.__waypoints = []
        if len(args) > 0:
            for wp in args[0]:
                self.add(wp)

    def __iter__(self):
        return iter(self.__waypoints)
    def __getitem__(self, index):
        return self.__waypoints[index]
    def __setitem__(self, index, value):
        while len(self.__waypoints) < index:
            self.__waypoints.append(Waypoint(0, 0))
        if index < len(self.__waypoints):
            self.__waypoints[index] = Waypoint(value)
        else:
            self.__waypoints.append(Waypoint(value))
    def __len__(self):
        return len(self.__waypoints)

    def __str__(self):
        result =  ""
        for wp in self:
            deg_wp = rad_to_deg(wp)
            result += "%f, %f" % (deg_wp[0], deg_wp[1])
            if hasattr(wp, 'comment'):
                result += " " + wp.comment
            result += "\n"
        return result
                      
    @property
    def waypoints(self):
        return self.__waypoints
    @waypoints.setter
    def waypoints(self, value):
        self.__waypoints = []
        for wp in value:
            self.__waypoints.append(Waypoint(wp))

    @property
    def segments(self):
        wp = iter(self.__waypoints)
        wp_from = wp.next()
        while True:
            wp_to = wp.next()
            yield wp_to.get_bearing_from(wp_from), wp_to
            wp_from = wp_to

    @property
    def length(self):
        l = 0
        for segment in self.segments:
            l += segment[0].r
        return l

    @vec_meth
    def add(self, waypoint):
        self.__waypoints.append(Waypoint(waypoint))

    def load_from_file(self, filename):
        f = open(filename, "r")
        self.__waypoints = []
        for line in f:
            # Split off comments
            line, sep, comment = line.partition("#")
            line = line.strip()
            if line != "": 
                vals = line.split(" ")
                la, lo = deg_to_rad(vals[:2])
                if len(vals) > 2:
                    ra = vals[2]
                else:
                    ra = Waypoint.range
                wp = Waypoint(la, lo, ra)
                wp.comment = comment.strip()
                self.__waypoints.append(wp)
        f.close()

    def save_to_kml(self, filename):
        filedir, file = os.path.split(filename)
        filebase, fileext = os.path.splitext(file)

        factory, kml = create_kml_document('Route: ' + filebase)
        
        route = factory.CreatePlacemark()
        route.set_name('Route')

#        style_elem = dom.createElement('Style')
#        style_elem.setAttribute('id', 'default')
#        doc.appendChild(style_elem)
#        iconstyle_elem = dom.createElement('IconStyle')
#        style_elem.appendChild(iconstyle_elem)
#        add_element_with_text(dom, iconstyle_elem, 'scale', '0.64')
#        icon_elem = dom.createElement('Icon')
#        iconstyle_elem.appendChild(icon_elem)
#        add_element_with_text(dom, icon_elem, \
        #                'href', 'http://maps.google.com/mapfiles/kml/paddle/blu-circle.png')

#        route_elem = dom.createElement('Placemark')
#        doc.appendChild(route_elem)
#        waypoints_elem = dom.createElement('Folder')
#        add_element_with_text(dom, waypoints_elem, 'name', 'Waypoints')
#        doc.appendChild(waypoints_elem)
#        add_element_with_text(dom, route_elem, 'name', 'Route')

#        description = 'UTC: ' + str(datetime.datetime.utcnow())
#        description += ' Length: ' + str(int(self.length / 1852)) + ' nm'
#        add_element_with_text(dom, route_elem, 'description', description)
#        line = dom.createElement('LineString')
#        route_elem.appendChild(line)
        #add_element_with_text(dom, line, 'extrude', '1')
        #        add_element_with_text(dom, line, 'tesselate', '1')
        #add_element_with_text(dom, line, 'altitudeMode', 'absolute')
        #        coordinates = dom.createElement('coordinates')
#        line.appendChild(coordinates)
#        coordinates_string = ''
#        for i, waypoint in enumerate(self.waypoints):
    #          coords = rad_to_deg(waypoint)
    #          coordinate_string = str(coords[1]) + ',' + str(coords[0]) + ',30 '
    #      coordinates_string += coordinate_string
    #      waypoint_elem = dom.createElement('Placemark')
    #      add_element_with_text(dom, waypoint_elem, 'styleUrl', '#default')
    #      waypoints_elem.appendChild(waypoint_elem)
    #      add_element_with_text(dom, waypoint_elem, 'name', 'Waypoint ' + str(i))
    #      point_elem = dom.createElement('Point')
    #      waypoint_elem.appendChild(point_elem)
    #      add_element_with_text(dom, point_elem, 'coordinates', coordinate_string)
    #      add_element_with_text(dom, point_elem, 'description', waypoint.comment)

    #    coordinates_text = dom.createTextNode(coordinates_string)
    #    coordinates.appendChild(coordinates_text)
        save_kml_document(kml, filename)

