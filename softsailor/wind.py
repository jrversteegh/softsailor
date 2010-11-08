import math

class Wind(object):
    def get(self, position, time = None):
        """Get wind direction at position an time"""
        # Default is a 1m/s southerly wind
        return math.pi, 1.0
