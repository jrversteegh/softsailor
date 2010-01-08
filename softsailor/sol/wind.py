from datetime import datetime, timedelta
import math

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

    def get(self, position, time):
        self.update(time)
        
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

    def verify_up_to_date(self):
        now = datetime.utcnow() 
        if now - self._last_verification > timedelta(minutes = 2):
            self.weather.verify_up_to_date()
            self._last_verification = now

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
            self.splined_frames.append(splined_frame)

