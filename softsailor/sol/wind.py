from datetime import datetime, timedelta
import math
from scipy.interpolate import bisplrep, bisplev, splrep, splev
import numpy as np

from softsailor.utils import *

class Wind:
    frame_i = 0
    frame_j = 0
    lat_range = 1.0
    lon_range = 1.0
    t_range = None
    def __init__(self, weather):
        self.weather = weather
        self._last_verification = datetime.utcnow()
        self.build_splines()
        
    def locate_frame(self, time):
        self.frame_j = 0
        try:
            while self.weather.frame_times[self.frame_j] < time:
                self.frame_j += 1
        except IndexError:
            pass
        self.frame_i = self.frame_j - 1
        if self.frame_j >= len(self.weather.frame_times):
            self.frame_j -= 1
            self.t_range = timedelta(hours = 1)
        else:
            self.t_range = self.weather.frame_times[self.frame_j] \
                    - self.weather.frame_times[self.frame_i]
        if self.frame_i < 0:
            self.frame_i = 0
        self.lat_range = self.weather.lat_max - self.weather.lat_min 
        self.lon_range = self.weather.lon_max - self.weather.lon_min 

    def get(self, position, time):
        if self.splined_frames != None and len(self.frame_times) > 3:
            return self.get_splined(position, time)
        else:
            return self.get_bilinear(position, time)

    def update(self, time):
        self.verify_up_to_date()

        if time < self.weather.frame_times[self.frame_i] \
               or time >= self.weather.frame_times[self.frame_j]:
            self.locate_frame(time)

    def get_indices(self, position):
        lat_frac = (position[0] - self.weather.lat_min) / float(self.lat_range)
        lat_frac *= self.weather.lat_n - 1
        lat_i = int(math.floor(lat_frac))
        lat_frac -= lat_i

        lon_frac = (position[1] - self.weather.lon_min) / float(self.lon_range)
        lon_frac *= self.weather.lon_n - 1
        lon_i = int(math.floor(lon_frac))
        lon_frac -= lon_i
        return lat_i, lon_i, lat_frac, lon_frac

    def get_splined(self, position, time):
        self.update(time)
        lat_i, lon_i, lat_frac, lon_frac = self.get_indices(position)
        if self.frame_i == 0:
            start_frame = 0
        else:
            start_frame = self.frame_i - 1
        end_frame = start_frame + 4
        while end_frame > len(self.frame_times):
            end_frame -= 1
            start_frame -= 1

        ts = self.frame_times[start_frame:end_frame]
        us = []
        vs = []
        t_frac = timedelta_to_seconds(time - self.weather.frame_times[self.frame_i]) \
                / timedelta_to_seconds(self.t_range)
 
        # Use spline eval between 1-2 rather than 0-1
        if lat_i > 0:
            lat_i -= 1
        if lon_i > 0:
            lon_i -= 1

        print "frame times: ", ts
        for i in range(start_frame, end_frame):
            tck = self.splined_frames[i][lat_i][lon_i][0]
            us.append(bisplev(position[0], position[1], tck))
            tck = self.splined_frames[i][lat_i][lon_i][1]
            vs.append(bisplev(position[0], position[1], tck))

        nts = np.array(ts)
        nus = np.array(us)
        nvs = np.array(vs)
        print "us: ", us
        print "vs: ", vs

        utck = splrep(ts, us)
        vtck = splrep(ts, vs)
        t = timedelta_to_seconds(time - self.start_time)
        print "time: ", time
        print "start time: ", self.start_time
        print "t: ", t
        
        u = splev(t, utck)
        v = splev(t, vtck)
        print "u: ", u
        print "v: ", v
        print "speed: ", math.sqrt(u * u + v * v) 
        lu = us[1] + t_frac * (us[2] - us[1])
        lv = vs[1] + t_frac * (vs[2] - vs[1])
        lint_speed = math.sqrt(lu * lu + lv * lv) 
        print "lint speed: ", lint_speed 

        return rectangular_to_polar((-lu, -lv))


    def get_bilinear(self, position, time):
        self.update(time)
        lat_i, lon_i, lat_frac, lon_frac = self.get_indices(position)
        lat_j = lat_i + 1
        lon_j = lon_i + 1

        t_frac = timedelta_to_seconds(time - self.weather.frame_times[self.frame_i]) \
                / timedelta_to_seconds(self.t_range)

        frame_1 = self.weather.frames[self.frame_i]
        frame_2 = self.weather.frames[self.frame_j]
        print "lat_i, lon_i: ", lat_i, lon_i
        print "lat_j, lon_j: ", lat_j, lon_j

        frame_1_u = frame_1[lat_i][lon_i][0] * (1 - lat_frac) * (1 - lon_frac) \
                + frame_1[lat_i][lon_j][0] * (1 - lat_frac) * lon_frac \
                + frame_1[lat_j][lon_i][0] * lat_frac * (1 - lon_frac) \
                + frame_1[lat_j][lon_j][0] * lat_frac * lon_frac 
        frame_1_v = frame_1[lat_i][lon_i][1] * (1 - lat_frac) * (1 - lon_frac) \
                + frame_1[lat_i][lon_j][1] * (1 - lat_frac) * lon_frac \
                + frame_1[lat_j][lon_i][1] * lat_frac * (1 - lon_frac) \
                + frame_1[lat_j][lon_j][1] * lat_frac * lon_frac 
        frame_2_u = frame_2[lat_i][lon_i][0] * (1 - lat_frac) * (1 - lon_frac) \
                + frame_2[lat_i][lon_j][0] * (1 - lat_frac) * lon_frac \
                + frame_2[lat_j][lon_i][0] * lat_frac * (1 - lon_frac) \
                + frame_2[lat_j][lon_j][0] * lat_frac * lon_frac 
        frame_2_v = frame_2[lat_i][lon_i][1] * (1 - lat_frac) * (1 - lon_frac) \
                + frame_2[lat_i][lon_j][1] * (1 - lat_frac) * lon_frac \
                + frame_2[lat_j][lon_i][1] * lat_frac * (1 - lon_frac) \
                + frame_2[lat_j][lon_j][1] * lat_frac * lon_frac 
        print "lat_frac: ", lat_frac
        print "lon_frac: ", lon_frac
        print "t_frac: ", t_frac
        print "u 1: ", frame_1_u
        print "v 1: ", frame_1_v
        print "u 2: ", frame_2_u
        print "v 2: ", frame_2_v
        u = frame_1_u * (1 - t_frac) + frame_2_u * t_frac
        v = frame_1_v * (1 - t_frac) + frame_2_v * t_frac
        wind = rectangular_to_polar((-u, -v))
        print "wind: ", wind

        return wind 

    def verify_up_to_date(self):
        now = datetime.utcnow() 
        if now - self._last_verification > timedelta(minutes = 2):
            self.weather.verify_up_to_date()
            self._last_verification = now

    def build_splines(self):
        self.frame_times = None
        self.splined_frames = None
        self.start_time = None
        w = self.weather
        if w.lat_n < 4 or w.lon_n < 4:
            return
        self.frame_times = []
        self.splined_frames = []
        self.start_time = self.weather.frame_times[0]
        for frame_time in self.weather.frame_times:
            self.frame_times.append(timedelta_to_seconds( \
                    frame_time - self.start_time))
        for frame in w.frames:
            x,y = np.mgrid[w.lat_min:w.lat_max:w.lat_n * 1j, \
                           w.lon_min:w.lon_max:w.lon_n * 1j]
            a = np.array(frame)
            u = a[:,:,0]
            v = a[:,:,1]
            splined_frame = []
            for i, frame_row in enumerate(frame[0:-3]):
                splined_row = []
                for j, wind in enumerate(frame_row[0:-3]):
                    u_spline = bisplrep(x[i:i+4,j:j+4], y[i:i+4,j:j+4], u[i:i+4,j:j+4])
                    v_spline = bisplrep(x[i:i+4,j:j+4], y[i:i+4,j:j+4], v[i:i+4,j:j+4])
                    splined_row.append((u_spline, v_spline))
                splined_frame.append(splined_row)
            #u_spline = bisplrep(x, y, u, s=0)
            #v_spline = bisplrep(x, y, v, s=0)
            #self.splined_frames.append((u_spline, v_spline))
            self.splined_frames.append(splined_frame)

