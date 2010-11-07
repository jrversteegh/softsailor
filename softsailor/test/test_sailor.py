import unittest

from softsailor.sailor import *

class TestSailor(unittest.TestCase):
    def setUp(self):
        self.sailor = Sailor()

    def testHasSail(self):
        self.assertTrue(hasattr(self.sailor, 'sail'))
        self.assertTrue(hasattr(self.sailor.sail, '__call__'))
