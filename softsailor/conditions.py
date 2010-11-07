class Condition(object):
    __wind = [0, 0]
    __current = [0, 0]
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

    @property
    def wind(self):
        return self.__wind
    @wind.setter
    def wind(self, value):
        self.__wind = list(value)

    @property
    def current(self):
        return self.__current
    @current.setter
    def current(self, value):
        self.__current = list(value)

class Conditions(object):
    def get_wind(self, lat, lon):
        return (0, 0)

    def get_current(self, lat, lon):
        return (0, 0)

    def get_condition(self, lat, lon):
        return Condition(self.get_wind(lat, lon), self.get_current(lat, lon))
        

