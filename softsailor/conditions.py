class Condition(object):
    wind = (0, 0)
    current = (0, 0)
    def __init__(self, *args, **kwargs):
        super(Condition, self).__init__()
        if len(args) > 0:
            self.wind = args[0]
            if len(args) > 1:
                self.current = args[1]
            else:
                self.current = kwargs['current']
        else:
            self.wind = kwargs['wind']

class Conditions(object):
    def get_wind(self, lat, lon):
        return (0, 0)

    def get_current(self, lat, lon):
        return (0, 0)

    def get_condition(self, lat, lon):
        return Condition(self.get_wind(lat, lon), self.get_current(lat, lon))
        

