class Map(object):
    def hit(self, segment):
        """Returns whether the segment crosses a land boundary"""
        return False

    def outer(self, segment):
        """Returns list of outermost points of land hit"""    
        return tuple()
