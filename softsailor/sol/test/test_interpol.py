from scipy.interpolate import splrep, splev
#import matplotlib.pyplot as plt
import numpy as np
import unittest

class TestInterpolation(unittest.TestCase):
    def testInterpol(self):
        x = [ 0, 1, 2, 3]
        y = [ 0, 0, 1, 1]
        nx = np.array(x)
        ny = np.array(y)
        tck = splrep(nx, ny)
        xs = np.linspace(0, 3, 20)
        ys = splev(xs, tck)
        print xs, ys
        for x, y in zip(xs, ys):
            print "%.3f" % y 
        

if __name__ == '__main__':
    unittest.main()
