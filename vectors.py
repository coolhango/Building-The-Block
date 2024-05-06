import math


class vec2:

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y


    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)


class vec3:

    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other):
        dx = abs(other.x - self.x)
        dy = abs(other.y - self.y)
        dz = abs(other.z - self.z)

        return math.sqrt(dx + dy + dz)


    def __add__(self, other):
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def lerp(self, other, t):
        loc_x = (1 - t) * self.x + t * other.x
        loc_y = (1 - t) * self.y + t * other.y
        loc_z = (1 - t) * self.z + t * other.z
        return vec3(loc_x, loc_y, loc_z)

    def __str__(self):
        return f"vec3({self.x}, {self.y}, {self.z})"