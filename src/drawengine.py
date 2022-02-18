from vector2 import *
from utils import *
from myparser import *

from threading import Thread
import time

class Singleton:
    window = None
    win = None
    input = None
    parser = None

class Sprite:
    def __init__(self, x = 0, y = 0, width = 50, height = 50, color = (255, 255, 255), add = True):
        if add:
            Singleton.window.add(self)

        self.position = Vector2(x, y)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.update_image()

        self.fill(color)

        self.rect.x = x - self.rect.width // 2
        self.rect.y = y - self.rect.height // 2

    def set_image(self, image):
        self.image = image
        self.update_image()

    def set_array(self, array):
        self.image = pygame.surfarray.make_surface(array)
        self.image = self.image.convert_alpha()
        self.update_image()

    def set_gradient(self, color1, color2, horizontal = (False, False, False)):
        grad = Utils.create_gradient(color1, color2, self.rect.width, self.rect.height, horizontal)
        self.set_array(grad)

    def update_image(self):
        self.rect = self.image.get_rect()
        self.original_image = self.image.copy()

    def fill(self, color):
        self.image.fill(color)

    def blit(self, image, pos = (0, 0)):
        self.image.blit(image, pos)

    def resize(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.update_image()

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.update_image()

    def draw(self):
        if self.image.get_locked():
            return
        Singleton.win.blit(self.image, (self.position - Vector2(self.rect.width, self.rect.height) / 2).pos())

class Label(Sprite):
    def __init__(self, x, y, width = 50, height = 50, color = (255, 255, 255), add = True):
        super().__init__(x, y, width, height, color, add)

        self.text = ''
        self.text_color = (0, 0, 0)

        self.target = Vector2(x, y)
        self.start = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.speed = 10
        self.friction = 0.93

        self.remove_after = False
        self.fade = 0

    def set_text(self, text, color = None, size = None):
        if color != None:
            self.text_color = color
        if size != None:
            font = pygame.font.SysFont('Comic Sans MS', size)
        else:
            font = pygame.font.SysFont('Comic Sans MS', 15)

        self.font = font
        self.text = text
        self.text_image = self.render_text()
        self.text_rect = self.text_image.get_rect()

    def render_text(self):
        text = self.text.split('\n')

        rendered = []
        for line in text:
            rendered.append(self.font.render(line, False, self.text_color))

        height = sum(i.get_height() for i in rendered)
        width = max(i.get_width() for i in rendered)

        result = pygame.Surface((width, height)).convert_alpha()
        result.fill((0, 0, 0, 0))
        y = 0
        for i in rendered:
            result.blit(i, (0, y))
            y += i.get_height()
        return result

    def move(self, x, y, speed, reverse = False):
        if self.remove_after:
            return

        self.target = Vector2(x, y)
        self.start = self.position.copy()
        self.speed = min(speed / 1000, 1)

        self.velocity = (self.target - self.start) * -(self.speed ** 0.65)
        self.friction = 0.93

        if reverse:
            self.velocity = -self.velocity

    def remove(self, x = None, y = None, speed = None, reverse = False):
        if x != None and y != None and speed != None:
            self.move(x, y, speed, reverse)
        self.remove_after = True

    def update(self):
        if self.target != self.position:
            delta = self.target - self.position

            self.velocity *= self.friction
            self.velocity += delta * self.speed
            self.position += self.velocity

            if self.fade != 0:
                scale = int(delta / (self.target - self.start) * 255)
                if self.fade == 1:
                    scale = 255 - scale
                scale = max(min(scale, 255), 0)
                self.image.set_alpha(scale)
                self.text_image.set_alpha(scale)

            if self.velocity.magnitude() + delta.magnitude() < 0.5 and self.friction != 1:
                if self.velocity.x != 0:
                    self.velocity.x = abs(self.velocity.x) / self.velocity.x * 0.06
                if self.velocity.y != 0:
                    self.velocity.y = abs(self.velocity.y) / self.velocity.y * 0.06
                self.speed *= 0.1
                self.friction = 1

            if delta.magnitude() < 1:
                self.on_arrival()

        self.rect.x = self.position.x - self.rect.width // 2
        self.rect.y = self.position.y - self.rect.height // 2

    def draw(self):
        super().draw()

        if hasattr(self, 'text_image') and not self.text_image.get_locked():
            Singleton.win.blit(self.text_image, (self.position - Vector2(self.text_rect.width, self.text_rect.height) / 2).pos())

    def on_arrival(self):
        if self.remove_after:
            Singleton.window.labels.remove(self)

        if self.fade:
            self.fade = 0
            self.image.set_alpha(255)
            self.text_image.set_alpha(255)

class Button(Label):
    def __init__(self, x, y, width = 50, height = 50, color = (255, 255, 255), function = None, add = True):
        super().__init__(x, y, width, height, color, add)

        if function == None:
            self.function = self.default_function
        else:
            self.function = function

        self.staytime = 0
        self.entered = False
        self.down = False

        self.active = True
        self.activate_after = False
        self.target = self.position.copy()

        self.overlay = pygame.Surface((self.rect.width, self.rect.height)).convert_alpha()
        self.overlay.fill((0, 0, 0, 1))

    def default_function(self):
        print(self, 'pressed')

    def update(self):
        super().update()

        if self.active:
            pos = Singleton.input.get_mouse_pos()
            if self.rect.collidepoint(pos):
                if not self.entered:
                    self.on_enter()
                self.on_stay()

            elif self.entered:
                self.on_exit()

    def on_enter(self):
        self.entered = True

    def on_stay(self):
        if not Singleton.window.disable_touch:
            if self.staytime < 10 and not self.down:
                self.blit(self.overlay)

            if Singleton.input.mouse_down(1) and not self.down:
                self.down = True

                self.overlay.fill((0, 0, 0, 30))
                self.image = self.original_image.copy()
                self.blit(self.overlay)
                self.overlay.fill((0, 0, 0, 1))

            elif Singleton.input.mouse_up(1) and self.down:
                self.function()
                self.on_exit()

        self.staytime += 1

    def on_exit(self):
        self.down = False
        self.entered = False
        self.staytime = 0

        self.image = self.original_image.copy()

    def on_arrival(self):
        super().on_arrival()

        if self.activate_after:
            self.active = True
            self.activate_after = False

class Window:
    def __init__(self, width = 500, height = 800):
        pygame.init()
        pygame.font.init()

        self.width, self.height = width, height

        self.win = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)

        pygame.display.set_caption('Сказки')
        icon = pygame.image.load('icon.ico')
        pygame.display.set_icon(icon)

        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN])

        self.clock = pygame.time.Clock()

        self.background = Sprite(self.width // 2, self.height // 2, add = False)
        self.vignette = Sprite(self.width // 2, self.height // 2, add = False)
        self.vignette.set_image(Utils.create_vignette((width, height), 1.35, 300000))

        self.color = [Color(0, 0, 0), Color(0, 0, 0)]
        self.labels = []

        self.running = True
        self.disable_touch = False
        self.screen_number = 0
        self.screenshot = ''

        Singleton.window = self
        Singleton.win = self.win
        Singleton.input = Input()
        Singleton.parser = Parser()

        self.initialized = 0
        Thread(target = self.init, daemon = True).start()

    def init(self):
        try:
            self.catalog = list(reversed(Singleton.parser.load_file('data/data')))
        except:
            self.initialized = -1
            return

        try:
            self.favourite = Singleton.parser.load_file('data/favourite')
        except:
            self.favourite = []
        self.initialized = 1

        try:
            self.tune_images()
            self.quest = Singleton.parser.load_file('data/quest')
        except:
            self.initialized = -2
            return
        self.initialized = 2

    def save_favourite(self):
        Singleton.parser.save_file(self.favourite, 'data/favourite')

    def tune_images(self):
        self.images = Singleton.parser.load_file('data/images')
        for image in self.images:
            self.images[image] = pygame.image.fromstring(self.images[image][0], self.images[image][1], 'RGB').convert()

        for tale in self.catalog:
            tale['img'] = pygame.image.fromstring(tale['img'][0], tale['img'][1], 'RGB').convert()

        self.images['clock'].set_colorkey((255, 255, 255))

        self.images['arrow_left'].set_colorkey((0, 0, 0))
        self.images['arrow_left'].set_alpha(40)

        self.images['correct'].set_colorkey((0, 0, 0))
        self.images['incorrect'].set_colorkey((0, 0, 0))

        self.images['arrow_right'] = pygame.transform.flip(self.images['arrow_left'], True, False)
        self.images['arrow_down'] = pygame.transform.rotate(self.images['arrow_left'], 90)
        self.images['arrow_up'] = pygame.transform.rotate(self.images['arrow_left'], -90)

    def add(self, label):
        self.labels.append(label)

    def change_background(self, color1, color2):
        image = Utils.create_gradient(color1, color2, self.width, self.height)
        self.background.set_array(image)
        self.background.blit(self.vignette.image)
        self.color = [color1, color2]

    def change_background_smooth(self, color1, color2, duraction):
        id = self.screen_number
        start = time.time()

        startcolor = self.color.copy()
        self.color = [color1, color2]

        delta1 = color1 - startcolor[0]
        delta2 = color2 - startcolor[1]

        while id == self.screen_number:
            time_ = time.time() - start
            if time_ >= duraction:
                image = Utils.create_gradient(color1.get(), color2.get(), self.width, self.height)
                self.background.set_array(image)
                self.background.blit(self.vignette.image)
                break

            delta = time_ / duraction
            image = Utils.create_gradient((startcolor[0] + delta1 * time_ / duraction).get(), (startcolor[1] + delta2 * time_ / duraction).get(), self.width, self.height)
            self.background.set_array(image)
            self.background.blit(self.vignette.image)

    def clear(self):
        side = 1
        for label in self.labels:
            side = -side
            label.remove(self.width * (max(0, side) + 0.5 * side), label.position.y, 3)

    def change(self, screen):
        self.screen_number += 1
        self.disable_touch = True
        self.clear()

        Thread(target = self.change_background_smooth, args = (screen.color[0], screen.color[1], 1), daemon = True).start()
        for show in screen.toshow:
            Thread(target = self.wait_screen, args = (show[0], show[1]), daemon = True).start()

    def wait_screen(self, function, delay):
        num = self.screen_number
        time.sleep(delay)

        if num != self.screen_number:
            return

        function()
        self.disable_touch = False

    def loop(self):
        self.running = True
        while self.running:
            wtime = time.time()
            self.clock.tick(60)
            Singleton.input.tick()

            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False

            Singleton.input.process_events(events)

            for label in self.labels:
                label.update()

            self.background.draw()
            for label in self.labels:
                label.draw()

            Singleton.input.end()
            pygame.display.flip()
