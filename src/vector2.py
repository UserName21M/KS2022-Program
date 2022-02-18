class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def pos(self):
        return (self.x, self.y)

    def copy(self):
        return Vector2(self.x, self.y)

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __str__(self):
        return str(self.x) + ', ' + str(self.y)

    def __add__(self, o):
        if type(o) == Vector2:
            return Vector2(self.x + o.x, self.y + o.y)
        else:
            return Vector2(self.x + o, self.y + o)

    def __sub__(self, o):
        if type(o) == Vector2:
            return Vector2(self.x - o.x, self.y - o.y)
        else:
            return Vector2(self.x - o, self.y - o)

    def __eq__(self, o):
        if type(o) == Vector2:
            return (self.x == o.x and self.y == o.y)
        else:
            return False

    def __ne__(self, o):
        if type(o) == Vector2:
            return (self.x != o.x or self.y != o.y)
        else:
            return False

    def __mul__(self, o):
        if type(o) == Vector2:
            return self.magnitude() * o.magnitude()
        else:
            return Vector2(self.x * o, self.y * o)

    def __truediv__(self, o):
        if type(o) == Vector2:
            m = o.magnitude()
            if m == 0:
                return 0
            return self.magnitude() / m
        else:
            return Vector2(self.x / o, self.y / o)

    def __neg__(self):
        return Vector2(-self.x, -self.y)
