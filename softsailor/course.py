"""
Course module

Contains info about a race course
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from softsailor.utils import *
from softsailor.route import Waypoint
from geofun import Vector, Position, Line

class Mark(Position):
    on_land = False
    to_port = False
    _target = None

    @property
    def target(self):
        if self._target is None:
            return self
        else:
            return self._target

    def set_target(self, value):
        self._target = value

class Finish(Position):
    left = Position()   
    right = Position()

class Course(object):
    mark_factory = Mark
    def __init__(self, *args, **kwargs):
        super(Course, self).__init__()
        self._marks = []
        self._start = Position()
        self._finish = Finish()
        if len(args) > 0:
            it = iter(args[0])
            try:
                p = it.next()
                self._start = Position(p[0], p[1])
                p = it.next()
                while True:
                    last_p = p
                    p = it.next()
                    self._marks.append(self.mark_factory(last_p[0], last_p[1]))
            except StopIteration:
                self._finish = Finish(p[0], p[1])
           
        
    @property
    def legs(self):
        last = self.start
        for mark in self.marks:
            yield Line(last, mark.target)
            last = mark.target
        yield Line(last, self.finish)

    @property
    def marks(self):
        return self._marks

    @property
    def start(self):
        return self._start

    @property
    def finish(self):
        return self._finish 
