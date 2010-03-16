import datetime as dt
from datetime import datetime, timedelta

from sol_xmlutil import *
from sol_settings import *

def two_float(str1, str2):
    return (float(str1), float(str2))

class Weather:
    def __init__(self):
        self.lat_min = 0
        self.lat_max = 0
        self.lat_range = 0
        self.lat_n = 0
        self.lat_step = 0

        self.lon_min = 0
        self.lon_max = 0
        self.lon_range = 0
        self.lon_n = 0
        self.lon_step = 0

        self.reltime_range = 0
        self.reltime_n = 0

        self.clear_frames()

        self._url = ''
        self._settings = None

    def clear_frames(self):
        self.frames = []
        self.reltimes = []
        self.datetimes = []
        self.start_datetime = datetime(dt.MAXYEAR, 1, 1)
    
    def get_url(self, settings):
        uri = settings.weather + '?token=' + settings.token
        dom = fetch_sol_document(settings.host, uri)
        url = get_child_text_value(dom.childNodes[0], 'url')
        dom.unlink()
        return url

    def load_data(self, url):
        self.clear_frames()

        self._url = url

        dom = fetch_sol_document_from_url(url)
        root = dom.childNodes[0]

        self.lat_min = deg_to_rad(root.getAttribute('lat_min'))
        self.lat_max = deg_to_rad(root.getAttribute('lat_max'))
        self.lat_range = self.lat_max - self.lat_min
        self.lat_n = int(root.getAttribute('lat_n_points'))
        self.lat_step = self.lat_range / (self.lat_n - 1)

        self.lon_min = deg_to_rad(root.getAttribute('lon_min'))
        self.lon_max = deg_to_rad(root.getAttribute('lon_max'))
        self.lon_range = self.lon_max - self.lon_min
        self.lon_n = int(root.getAttribute('lon_n_points'))
        self.lon_step = self.lon_range / (self.lon_n - 1)

        frames_parent = get_element(root, 'frames')
        frames = frames_parent.getElementsByTagName('frame')
        for frame in frames:
            self.add_frame(frame)

        self.reltime_range = self.reltimes[-1]
        self.reltime_n = len(self.reltimes)

    def add_frame(self, frame):
        target_time_text = frame.getAttribute('target_time')
        target_time = datetime.strptime(target_time_text, '%Y/%m/%d %H:%M:%S')
        self.datetimes.append(target_time)
        if target_time < self.start_datetime:
            self.start_datetime = target_time
        self.reltimes.append(
                 timedelta_to_seconds(target_time - self.start_datetime))
        u_text = get_child_text_value(frame, 'U')
        v_text = get_child_text_value(frame, 'V')
        u_rows = u_text.split(';')
        v_rows = v_text.split(';')
        grid = []
        for u_row, v_row in zip(u_rows, v_rows):
            if u_row.strip() != '' and v_row.strip() != '':
                us = u_row.split()
                vs = v_row.split()
                grid.append(map(two_float, vs, us))
        # The u,v grid is transposed with respect to the x,y frame
        frame = zip(*grid)
        self.frames.append(frame)

    def load(self, settings):
        url = self.get_url(settings)
        self.load_data(url)
        self._settings = settings

    def update_when_required(self):
        if self._settings == None:
            return False
        url = self.get_url(self._settings)
        if url != self._url:
            self.load_data(url)
            return True
        else:
            return False


