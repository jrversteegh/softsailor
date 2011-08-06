"""
Classes module

Contains utility classes
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

import math
import numpy as np
from datetime import datetime, timedelta

from utils import *


class Logable(object):
    def __init__(self, *args, **kwargs):
        super(Logable, self).__init__()
        self._log_data = []
        self.fmtrs = []

    def log(self, log_str, *record_fields):
        self._log_data.append((datetime.utcnow(), log_str, record_fields))
        while len(self.fmtrs) < len(record_fields):
            self.fmtrs.append(str)

    def save_log(self, filename):
        f = open(filename, "w")
        for record in self._log_data:
            f.write(record[0].strftime(time_format) + ", " + record[1])
            for i, field in enumerate(record[2]):
                f.write(", " + self.fmtrs[i](field).encode('utf-8'))
            f.write("\n")
        f.close()

    def print_log(self, lines=0):
        for record in self._log_data[-lines:]:
            fields = []
            for i, field in enumerate(record[2]):
                fields.append(self.fmtrs[i](field))
            print record[0].strftime(time_format), record[1], fields

    @property
    def records(self):
        return self._log_data

class PolarData(object):
    def __init__(self, *args, **kwargs):
        super(PolarData, self).__init__()
        self.speeds = []
        self.angles = []
        # Data is organized as list of speeds per angle
        self.data = []

    def save_to_file(self, filename):
        f = open(filename, "w")
        for i, angle in enumerate(self.angles):
            f.write('%.2f' % rad_to_deg(angle) + ':')
            for j, wind_speed in enumerate(self.speeds):
                f.write(' %.2f:%.2f' % (ms_to_kn(wind_speed),
                                        ms_to_kn(self.data[i][j])))
            f.write("\n")
        f.close()


