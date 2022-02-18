from drawengine import *
from catalog import Catalog
from quizscreen import Quizscreen

class Mainscreen:
    def __init__(self):
        self.window = Singleton.window
        self.color = [Color(100, 100, 200), Color(200, 200, 250)]

        self.toshow = [(self.show, 1), (self.show_delayed, 3)]

    def show(self):
        button = Button(self.window.width / 2 - 100, self.window.height + 50, width = 200, height = 100, function = self.catalog)
        button.set_gradient((220, 220, 220), (110, 110, 220), (False, True, True))
        button.set_text('Каталог', (255, 255, 255), 40)
        button.move(self.window.width / 2, 175, 3, True)

        button = Button(self.window.width / 2 + 50, self.window.height + 50, width = 200, height = 100, function = self.settings)
        button.set_gradient((160, 220, 220), (110, 110, 220), (False, True, True))
        button.set_text('Викторина', (255, 255, 255), 35) # Настройки
        button.move(self.window.width / 2, 300, 3, True)

        button = Button(self.window.width / 2 - 50, self.window.height + 50, width = 200, height = 100, function = self.update)
        button.set_gradient((220, 160, 220), (110, 160, 220), (False, True, True))
        button.set_text('Обновление', (255, 255, 255), 30)
        button.move(self.window.width / 2, 425, 3, True)

        button = Button(self.window.width / 2 + 100, self.window.height + 50, width = 200, height = 100, function = self.quit)
        button.set_gradient((160, 220, 220), (110, 110, 220), (False, True, True))
        button.set_text('Выход', (255, 255, 255), 35)
        button.move(self.window.width / 2, 550, 3, True)

    def show_delayed(self):
        button = Button(self.window.width / 2, self.window.height + 50, width = 100, height = 50, function = self.credits)
        button.set_gradient((220, 220, 220), (160, 160, 220), (False, True, True))
        button.set_text('Создатели', (255, 255, 255), 15)
        button.move(self.window.width / 2, 650, 3, True)

    def quit(self):
        self.window.running = False

    def catalog(self):
        self.window.change(Catalog())

    def settings(self):
        self.window.change(Quizscreen())

    def credits(self):
        self.window.change(Credits())

    def update(self):
        self.window.change(Updatescreen())

class Startscreen:
    def __init__(self):
        self.window = Singleton.window
        self.parser = Singleton.parser
        self.color = [Color(170, 170, 170), Color(220, 220, 220)]

        self.toshow = [(self.show, 0), (self.loop, 0.1)]
        self.label = None
        self.frame = 0

    def show(self):
        self.label = Label(self.window.width / 2, -100, width = self.window.width - 20, height = 40)
        self.label.set_gradient((110, 110, 110), (200, 200, 200), (True, True, True))
        self.label.set_text('Подгружаем каталог', (50, 50, 50), 20)
        self.label.move(self.window.width / 2, self.window.height / 2, 6, True)

    def loop(self):
        while self.window.initialized == 0:
            self.update_dots('Подгружаем каталог')

        self.label.set_text('Обрабатываем изображения', (50, 50, 50), 20)

        while self.window.initialized == 1:
            self.update_dots('Обрабатываем изображения')

        if self.window.initialized == -1:
            self.window.change(Updatescreen(error = 1))
            return
        elif self.window.initialized == -2:
            self.window.change(Updatescreen(error = 2))
            return

        self.window.change(Mainscreen())
        self.label.image = self.label.image.convert()
        self.label.fade = -1

    def update_dots(self, text):
        self.frame += 1
        self.label.set_text(text + '.' * (self.frame % 4), (50, 50, 50), 20)
        time.sleep(0.5)

class Updatescreen:
    def __init__(self, error = 0):
        self.window = Singleton.window
        self.parser = Singleton.parser
        self.color = [Color(100, 200, 100), Color(220, 255, 170)]

        self.toshow = [(self.show1, 0.2), (self.show2, 0.4), (self.show3, 0.6), (self.show4, 1)]
        self.error = error

    def show1(self):
        if self.error != 0:
            label = Label(self.window.width / 2, -100, width = self.window.width, height = 40)
            label.set_gradient((180, 150, 110), (255, 200, 170), (True, True, True))
            label.move(self.window.width / 2, self.window.height / 2 - 200, 6, True)

            if self.error == 1:
                label.set_text('Произошла ошибка при загрузке каталога', (50, 50, 50), 20)
            elif self.error == 2:
                label.set_text('Произошла ошибка при загрузке файлов', (50, 50, 50), 20)

        label = Label(self.window.width / 2, -100, width = self.window.width, height = 40)
        label.set_gradient((140, 180, 110), (220, 255, 170), (True, True, True))
        label.move(self.window.width / 2, self.window.height / 2 - 150, 6, True)

        if self.error == 1:
            label.set_text('Необходимо обновление', (50, 50, 50), 20)
        elif self.error == 0:
            label.set_text('Вы обновите каталог сказок', (50, 50, 50), 20)
        elif self.error == 2:
            label.set_text('Требуется переустановить приложение', (50, 50, 50), 20)

        if self.error == 2:
            button = Button(self.window.width + 150, self.window.height / 2 + 100, width = 75, height = 50, function = self.no)
            button.set_gradient((180, 150, 110), (255, 220, 170), (False, True, True))
            button.set_text('Выйти', (255, 255, 255), 20)
            button.move(self.window.width / 2, self.window.height / 2 + 100, 3)

    def show2(self):
        if self.error == 2:
            return

        label = Label(self.window.width / 2, -100, width = self.window.width, height = 40)
        label.set_gradient((140, 180, 110), (220, 255, 170), (True, True, True))
        label.set_text('Для этого требуется интернет соединение', (50, 50, 50), 20)
        label.move(self.window.width / 2, self.window.height / 2 - 100, 6, True)

    def show3(self):
        if self.error == 2:
            return

        label = Label(self.window.width / 2, -100, width = self.window.width, height = 40)
        label.set_gradient((140, 180, 110), (220, 255, 170), (True, True, True))
        label.set_text('Может занять некоторое время', (50, 50, 50), 20)
        label.move(self.window.width / 2, self.window.height / 2 - 50, 6, True)

    def show4(self):
        if self.error == 2:
            return

        label = Label(self.window.width / 2, -100, width = self.window.width, height = 40)
        label.fill((0, 0, 0, 0))
        label.set_text('Начать обновление?', (50, 50, 50), 25)
        label.move(self.window.width / 2, self.window.height / 2 + 50, 6, True)

        button = Button(-150, self.window.height / 2 + 100, width = 75, height = 50, function = self.yes)
        button.set_gradient((110, 180, 140), (170, 255, 220), (False, True, True))
        button.set_text('Да', (255, 255, 255), 20)
        button.move(self.window.width / 3, self.window.height / 2 + 100, 3)

        button = Button(self.window.width + 150, self.window.height / 2 + 100, width = 75, height = 50, function = self.no)
        button.set_gradient((180, 150, 110), (255, 220, 170), (False, True, True))
        button.set_text('Нет', (255, 255, 255), 20)
        button.move(self.window.width / 3 * 2, self.window.height / 2 + 100, 3)

    def yes(self):
        Thread(target = self.parser.update, daemon = False).start()
        self.window.change(Loadingscreen())

    def no(self):
        if self.error != 0:
            self.window.running = False
        else:
            self.window.change(Mainscreen())

class Loadingscreen:
    def __init__(self):
        self.window = Singleton.window
        self.parser = Singleton.parser
        self.color = [Color(170, 170, 170), Color(220, 220, 220)]

        self.toshow = [(self.show, 0), (self.loop, 0)]
        self.progressbar = None

    def show(self):
        self.progressbar = Label(self.window.width / 2, -100, width = self.window.width - 20, height = 40)
        self.progressbar.set_gradient((110, 110, 110), (200, 200, 200), (True, True, True))
        self.progressbar.move(self.window.width / 2, self.window.height / 2, 6, True)

    def loop(self):
        while self.progressbar == None: # not hasattr(self, 'progressbar'):
            time.sleep(0.1)

        was, progress = -1, 0
        while progress < 1:
            progress = round(self.parser.progress, 2)
            if was != progress:
                loading = pygame.Surface((progress * (self.window.width - 40), 28))
                loading.fill((80, 80, 80))
                self.progressbar.blit(loading, (10, 6))
            was = progress
            time.sleep(0.1)

        time.sleep(0.5)
        self.window.change(Startscreen())

        self.window.initialized = 0
        Thread(target = self.window.init, daemon = True).start()

class Credits:
    def __init__(self):
        self.window = Singleton.window
        self.color = [Color(255, 255, 255), Color(160, 160, 160)]

        self.toshow = [(self.show, 0.5), (self.show_delayed, 2)]

    def show(self):
        button = Button(-100, self.window.height - 50, width = 100, height = 50, function = self.back)
        button.set_gradient((220, 220, 220), (180, 180, 180), (True, True, True))
        button.set_text('Назад', (255, 255, 255), 20)
        button.move(75, self.window.height - 50, 3)

        label = Label(self.window.width / 2, self.window.height + 50, color = (0, 0, 0, 0))
        label.set_text('Все сделал Глазунов Матвей', (70, 70, 70), 30)
        label.move(self.window.width / 2, 300, 2)

    def show_delayed(self):
        label = Label(self.window.width / 2, self.window.height + 50, color = (0, 0, 0, 0))
        label.set_text('Специально для фестиваля "Компьютерная страна 2022"', (140, 70, 70), 13)
        label.move(self.window.width / 2, 335, 1.5)

    def back(self):
        self.window.change(Mainscreen())
