class Map(object):
    def hit(self, line):
        """Returns whether the segment crosses a land boundary"""
        return False

    def outer(self, line):
        """Returns tuple of outermost points of land hit"""    
        return tuple()
