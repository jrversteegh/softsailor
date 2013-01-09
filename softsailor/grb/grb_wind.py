"""
Grib wind module

Contains implementation wind provider for grib data
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from datetime import datetime, timedelta
import math
import os.path
import numpy as np
import pygrib as pg

from softsailor.utils import *
from softsailor.wind import *


class GribWind(InterpolledWind):
    _filename = ''
    _filedate = 0
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._filename = args[0]
        else:
            try:
                self._filename = kwargs['filename']
            except KeyError:
                pass
        super(GribWind, self).__init__(*args, **kwargs)

    def update(self):
        self.update_from_file()

    def update_from_file(self, filename=''):
        if filename:
            self._filename = filename
        if self._filename and os.path.isfile(self._filename):
            self._load_from(self._filename)
            self._filedate = os.path.getmtime(self._filename)

    def _load_from(self, filename):
        grb = pg.open(filename)
        # Dictionary with data with time as key and a dictionary with properties
        # as values
        data = {}
        for msg in grb:
            fcst = timedelta(hours=msg.unitOfTimeRange * msg.P2)
            t = msg.analDate + fcst
            # Only handle u and v messages
            if msg.paramId == 165 or msg.paramId == 166:








