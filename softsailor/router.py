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

    def construct_legs(self):
        self.legs = []
        for course_leg in self.course.legs:
            outers = self.chart.outer_lines(course_leg)
            if len(outers) > 0:
                routes = []
                for outer in outers:
                    route = Route()
                    route.add(course_leg.p1)
                    for p in outer:
                        route.add(p)
                    route.add(course_leg.p2)
                    router.append(route)
                self.legs.append(min(routes, key=lambda r: r.length))
            else:
                route = Route((course_leg.p1, course_leg.p2))
                self.legs.append(route)

    def construct_course(self):
        self.course = Route()
        for leg in self.legs:
            self.course += leg

