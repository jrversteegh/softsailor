
class Motion(object):
    speed = 0
    course = 0

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            course = args[0]
            speed = args[1]
        elif len(args) > 0:
            course = args[0][0]
            speed = args[0][1]

    @property
    def velocity(self):
        return (self.course, self.speed) 
    @velocity.setter
    def velocity(self, value):
        self.course = value[0]
        self.speed = value[1]
