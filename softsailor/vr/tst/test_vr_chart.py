import os
import unittest
import testing_helper


from softsailor.utils import *
from softsailor.route import Route
from softsailor.chart import Path
from softsailor.vr.vr_chart import *
from softsailor.vr.vr_settings import Settings

from geofun import Position, Vector

dirname = os.path.dirname(os.path.abspath(__file__))

testing_helper.setup_log('test_vr_chart')


class TestChart(unittest.TestCase):
    def setUp(self):
        self.chart = Chart()

    @unittest.skipIf(testing_helper.offline, "Requires sailonline connection")
    def testLoad(self):
        pass

    def testHit(self):
        pass

    def testSaveToKml(self):
        pass



if __name__ == '__main__':
    unittest.main()
