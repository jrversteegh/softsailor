"""
Router module

Contains an object that produces routes
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from route import Route
from utils import angle_diff

class Router(object):
    def __init__(self, *args, **kwargs):
        super(Router, self).__init__()
        self.course = kwargs['course']
        try:
            self.chart = kwargs['chart']
        except KeyError:
            self.chart = kwargs['map']
        try:
            self.boat = kwargs['boat']
        except KeyError:
            self.boat = None

        self.construct_legs()

    def valid_route(self, route, marks=None):
        if marks is None:
            mks = self.course.marks
        else:
            mks = []
            for mark in marks:
                for mk in self.course.marks:
                    if mk == mark:
                        mks.append(mk)
        ans = [0 for mk in mks]
        for l in route.lines:
            for i, mk in enumerate(mks):
                v1 = mk - l.p1
                v2 = mk - l.p2
                ans[i] += angle_diff(v2.a, v1.a)
        for a, mk in zip(ans, mks):
            if mk.to_port and a >= 0:
                return False
            if not mk.to_port and a <= 0:
                return False
        return True


    def construct_legs(self):
        self.legs = []
        for course_leg in self.course.legs:
            outers = self.chart.outer_points(course_leg)
            routes = []
            for outer in outers:
                route = Route(outer, course_leg)
                if self.valid_route(route, (course_leg.p1, course_leg.p2)):
                    routes.append(route)
            routes.sort(key=lambda r: r.length)
            self.legs.append(routes)

    def construct_course(self):
        self.course = Route()
        for leg in self.legs:
            self.course += leg

