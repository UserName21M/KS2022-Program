import pygame
import numpy as np

class Utils:
    def _gradient2d(start, end, width, height, horizontal):
        if horizontal:
            return np.tile(np.linspace(start, end, width), (height, 1)).T
        else:
            return np.tile(np.linspace(start, end, height), (width, 1))

    def create_gradient(start, end, width, height, horizontal = (False, False, False)): # https://note.nkmk.me/en/python-numpy-generate-gradation-image/
        image = np.zeros((width, height, len(start)), dtype = np.uint8)

        for i, (start_, end_, horizontal_) in enumerate(zip(start, end, horizontal)):
            image[:, :, i] = Utils._gradient2d(start_, end_, width, height, horizontal_)

        return image

    def create_vignette(size, intensity, smooth):
        scale = size[0] / size[1]
        centre = (size[0] / 2, size[1] / 2)

        vignette = pygame.Surface(size, pygame.SRCALPHA, 32)
        vignette = vignette.convert_alpha()

        for x in range(size[0]):
            for y in range(size[1]):
                dx = (centre[0] - x) / scale
                dy = centre[1] - y
                dist = (dx ** 2 + dy ** 2) ** intensity

                val = min(255, int(dist / smooth))
                vignette.set_at((x, y), (0, 0, 0, val))

        return vignette

    def add_frame(image, color, width):
        size = (image.get_width(), image.get_height())
        result = pygame.Surface(size)
        result.fill(color)

        image = pygame.transform.scale(image, (size[0] - width * 2, size[1] - width * 2))
        result.blit(image, (width, width))

        return result

    def cut_text(text, font, width, height, dots = True):
        result = ''

        text = text.split(' ')
        _height, _width = 0, 0
        for word in text:
            size = font.size(word)
            _width += size[0]

            if _width > width:
                _width = 0
                _height += size[1]

                if _height > height:
                    if dots:
                        result += '....'
                    break
                else:
                    result += '\n'
            result += word + ' '
        return result[:-1]

class Input:
    def __init__(self):
        self.mdown = []
        self.mup = []

        self.wkeys = pygame.key.get_pressed()
        self.wmdown = []

        self.mx = 0
        self.my = 0

        self.last_events = []

    def tick(self):
        self.keys = pygame.key.get_pressed()
        self.mx, self.my = pygame.mouse.get_pos()

    def end(self):
        self.wkeys = self.keys
        self.wmdown = self.mdown.copy()

    def process_events(self, events):
        self.mdown.clear()
        self.mup.clear()

        self.last_events = events
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.mdown.append(e.button)
            elif e.type == pygame.MOUSEBUTTONUP:
                self.mup.append(e.button)

    def is_pressed(self, key):
        return self.keys[key]

    def just_pressed(self, key):
        return (self.keys[key] and not self.wkeys[key])

    def mouse_down(self, button):
        return (button in self.mdown)

    def mouse_up(self, button):
        return (button in self.mup)

    def mouse_just_down(self, button):
        return (button in self.mdown and not button in self.wmdown)

    def get_mouse_pos(self):
        return self.mx, self.my

class Color:
    def __init__(self, r = 0, g = 0, b = 0):
        self.r = r
        self.g = g
        self.b = b

    def get(self):
        return (int(self.r), int(self.g), int(self.b))

    def copy(self):
        return Color(self.r, self.g, self.b)

    def __str__(self):
        return str(self.r) + ', ' + str(self.g) + ', ' + str(self.b)

    def __add__(self, o):
        if type(o) == Color:
            return Color(self.r + o.r, self.g + o.g, self.b + o.b)
        else:
            return Color(self.r + o, self.g + o, self.b + o)

    def __sub__(self, o):
        if type(o) == Color:
            return Color(self.r - o.r, self.g - o.g, self.b - o.b)
        else:
            return Color(self.r - o, self.g - o, self.b - o)

    def __eq__(self, o):
        if type(o) == Color:
            return (self.r == o.r and self.g == o.g and self.b == o.b)
        else:
            return (self.r == o and self.g == o and self.b == o)

    def __ne__(self, o):
        if type(o) == Color:
            return (self.r != o.r or self.g != o.g or self.b != o.b)
        else:
            return (self.r != o or self.g != o or self.b != o)

    def __mul__(self, o):
        return Color(self.r * o, self.g * o, self.b * o)

    def __truediv__(self, o):
        if o == 0:
            return Color(0, 0, 0)
        else:
            return Color(self.r / o, self.g / o, self.b / o)
