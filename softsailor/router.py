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
from utils import angle_diff, pos_to_str

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

    def valid_route(self, route, targets=None):
        if targets is None:
            mks = self.course.marks
        else:
            mks = []
            for target in targets:
                for mk in self.course.marks:
                    if mk.target == target:
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
        for i, course_leg in enumerate(self.course.legs):
            outers = self.chart.find_paths(course_leg)
            routes = []
            for outer in outers:
                route = Route(outer)
                if self.valid_route(route, (course_leg.p1, course_leg.p2)):
                    routes.append(route)
                else:
                    pass
                    #print "Route not valid"
            routes.sort(key=lambda r: r.length)
            for j in xrange(len(routes) - 2, -1, -1):
                if routes[j] == routes[j + 1]:
                    del routes[j]
            if not routes:
                raise Exception('Failed to find route on leg %d' % i + 1)
            self.legs.append(routes)

    @property
    def course_routes(self):
        if self.legs:
            route_count = 1
            for leg in self.legs:
                route_count *= len(leg)
            count_divider = max(1, round(1024, 1 / len(self.legs)))
            def max_routes(leg):
                return max(2, len(leg) / count_divider)

            result = self.legs[0][:max_routes(self.legs[0])]
            for leg in self.legs[1:]:
                new_result = []
                for res in result:
                    for rt in leg[:max_routes(leg)]:
                        new_route = res + rt
                        new_result.append(new_route)
                result = new_result
        else:
            result = []
        result.sort(key=lambda r: r.length)
        return result


