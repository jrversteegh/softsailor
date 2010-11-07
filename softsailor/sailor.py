
class Sailor(object):
    """Handles sailing a boat along a route"""
    def __init__(self, *args, **kwargs):
        super(Sailor, self).__init__()
        self.boat = args[0]
        self.controller = args[1]
        self.updater = args[2]

    def sail(self):
        self.updater.update()
        new_heading = self.get_heading()
        if abs(new_heading - self.boat.heading) > 0.1:
            self.controller.do_steer(new_heading)
        
