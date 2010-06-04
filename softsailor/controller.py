from boat import Boat

class Controller(object):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        
    def steer_heading(self, heading):
        pass

    def steer_windangle(self, windangle):
        pass


