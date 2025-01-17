import math

class Line:
    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, x0, y0, x1, y1):
        if x0 < x1:
            self.x0 = x0
            self.y0 = y0
            self.x1 = x1
            self.y1 = y1
        else:
            self.x0 = x1
            self.y0 = y1
            self.x1 = x0
            self.y1 = y0
    
    def configuration(self):
        return Line.HORIZONTAL if  abs(self.x0-self.x1) < abs(self.y0-self.y1) else Line.VERTICAL

    def __str__(self):
        return "(" + str(self.x0) + ", " + str(self.y0) + ") (" + str(self.x1) + ", " + str(self.y1) + ")"
    
    def length(self):
        return math.sqrt((self.x0-self.x1) ** 2 + (self.y0-self.y1) ** 2)

    def coordinates(self):
      return ((self.x0, self.y0), (self.x1, self.y1))

    def coordinates_as_int(self):
      return ((int(self.x0), int(self.y0)), (int(self.x1), int(self.y1)))