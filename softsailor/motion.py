
class Motion(object):
    speed = 0
    course = 0
    drift = 0

    @property
    def velocity(self):
        return (self.course, self.speed) 
    @velocity.setter
    def velocity(self, value):
        self.course = value[0]
        self.speed = value[1]
