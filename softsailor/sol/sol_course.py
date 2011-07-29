"""
Sol course module

Contains info about a sol race course
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from softsailor.utils import *
from softsailor.route import Waypoint
from softsailor.course import *
from geofun import Vector, Position, Line

class SolMark(Mark):
    target_vector = Vector()

class SolCourse(Course):
    def __init__(self, *args, **kwargs):
        super(SolCourse, self).__init__()
        chart = None
        if len(args) > 0:
            waypoints = args[0]
        if len(args) > 1:
            finish_radius = args[1]
        if len(args) > 2:
            chart = args[2]
        try:
            waypoints = kwargs['waypoints']
        except KeyError:
            pass
        try:
            finish_radius = kwargs['finish_radius']
        except KeyError:
            pass
        try:
            chart = kwargs['map']
        except KeyError:
            pass
        try:
            chart = kwargs['chart']
        except KeyError:
            pass
        self._chart = chart
        self._start = Position(waypoints[0][0], waypoints[0][1])
        self._finish = Finish(waypoints[-1][0], waypoints[-1][1])

        # Enrich waypoints to turn them into marks 
        for i in range(1, len(waypoints) - 1):
            prev = Position(waypoints[i - 1][0], waypoints[i - 1][1])
            mark = Mark(waypoints[i][0], waypoints[i][1])
            nxt = Position(waypoints[i + 1][0], waypoints[i + 1][1])
            v1 = mark - prev
            v2 = nxt - mark
            a1 = angle_diff(v2.a, v1.a)
            mark.to_port = a1 < 0
            mark.on_land = self.get_on_land(mark)
            if mark.to_port:
                a2 = normalize_angle_2pi(v1.a + 0.5 * (a1 + pi))
            else:
                a2 = normalize_angle_2pi(v1.a + 0.5 * (a1 - pi))
            mark.target_vector = Vector(a2, 1)
            if mark.on_land:
                dist = 0
                for i in range(-49, 50):
                    a = a2 + i * (0.01 + 0.003 * math.fabs(a1))
                    perp = Line(mark, mark + Vector(a, 25000))
                    chart_segment, intersect = self._chart.intersect(perp)
                    v = intersect - mark
                    if v.r > dist:
                        dist = v.r
                        intersection = intersect
                mark.target = intersection + mark.target_vector * 42
            else:
                mark.target = mark + mark.target_vector * 42
            self._marks.append(mark)

        # Construct finish line
        finish_leg = self._finish - Position(waypoints[-2][0], waypoints[-2][1])
        self._finish.left = self._finish + Vector(finish_leg.a - half_pi, finish_radius)
        self._finish.right = self._finish + Vector(finish_leg.a + half_pi, finish_radius)


    def get_on_land(self, position):
        if self._chart is not None:
            line = Line(self._start, position)
            hits = self._chart.intersections(line)
            return len(hits) % 2 == 1
        else:
            return False

    def save_to_kml(self, filename):
        filedir, file = os.path.split(filename)
        filebase, fileext = os.path.splitext(file)

        kml, doc = create_kml_document('Race course: ' + filebase)

        factory = kmldom.KmlFactory_GetFactory()
        
        marks = factory.CreateFolder()
        marks.set_name('Marks')

        start = create_point_placemark(
                'Start', rad_to_deg(self._start[0]), rad_to_deg(self._start[1]))
        start.set_description('Start')
        start.set_styleurl('#default')
        marks.add_feature(start)

        for i, mk in enumerate(self.marks):
            mark = create_point_placemark('Mark ' + str(i + 1), \
                    rad_to_deg(mk[0]), rad_to_deg(mk[1]))
            if mk.to_port:
                orient_str = 'Keep to port'
            else:
                orient_str = 'Keep to starboard'
            mark.set_description('Mark %d %s' % (i + 1, orient_str))
            mark.set_styleurl('#default')
            marks.add_feature(mark)
            p1 = list(mk)
            p2 = list(mk.target)
            ln = (rad_to_deg(p1), rad_to_deg(p2))
            target = create_line_placemark('Target ' + str(i + 1), ln)
            marks.add_feature(target)

        finish = create_point_placemark(
                'Finish', rad_to_deg(self._finish[0]), rad_to_deg(self._finish[1]))
        finish.set_description('Finish')
        finish.set_styleurl('#default')
        marks.add_feature(finish)
        p1 = list(self._finish.left)
        p2 = list(self._finish.right)
        ln = (rad_to_deg(p1), rad_to_deg(p2))
        fl = create_line_placemark('Finish line', ln)
        marks.add_feature(fl)
        
        description = 'Race marks'
        doc.set_description(description)
        doc.add_feature(marks)
        
        save_kml_document(kml, filename)

