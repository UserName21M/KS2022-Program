from drawengine import *
import screens

import random
from copy import deepcopy

from tkinter import Tk
from tkinter import filedialog

Tk().withdraw()

class Quizscreen:
    page = 0
    quest = None
    correct = 0

    def __init__(self):
        self.window = Singleton.window
        self.color = [Color(170, 170, 140), Color(230, 230, 170)]

        self.toshow = [(self.show_back, 0.5), (self.show, 0.5)]
        self.labels = []

    def show_back(self):
        button = Button(50, self.window.height + 50, width = 100, height = 50, function = self.back)
        button.set_gradient((250, 250, 200), (200, 200, 150), (False, True, True))
        button.set_text('Выход', (255, 255, 255), 20)
        button.move(75, self.window.height - 50, 3)

    def show(self):
        if Quizscreen.quest != None:
            label = Label(self.window.width / 2, -150)
            label.fill((0, 0, 0, 0))
            label.set_text('Вы хотите продолжить?', (255, 255, 255), 35)
            label.move(self.window.width / 2, self.window.height / 2 - 50, 3)
            self.labels.append(label)

            button = Button(-150, self.window.height / 2 + 100, width = 75, height = 50, function = self.yes)
            button.set_gradient((110, 180, 140), (170, 255, 220), (False, True, True))
            button.set_text('Да', (255, 255, 255), 20)
            button.move(self.window.width / 3, self.window.height / 2 + 50, 3)
            self.labels.append(button)

            button = Button(self.window.width + 150, self.window.height / 2 + 100, width = 75, height = 50, function = self.no)
            button.set_gradient((180, 150, 110), (255, 220, 170), (False, True, True))
            button.set_text('Нет', (255, 255, 255), 20)
            button.move(self.window.width / 3 * 2, self.window.height / 2 + 50, 3)
            self.labels.append(button)

            return

        label = Label(self.window.width / 2, -150, width = 300, height = 120)
        label.fill((0, 30, 30, 10))
        label.set_text('Викторина', (255, 235, 210), 50)
        label.move(self.window.width / 2, self.window.height / 2 - 300, 3)
        self.labels.append(label)

        label = Label(self.window.width / 2, -150)
        label.fill((0, 0, 0, 0))
        label.set_text('Выберите сложность:', (255, 255, 255), 35)
        label.move(self.window.width / 2, self.window.height / 2 - 150, 3)
        self.labels.append(label)

        button = Button(self.window.width / 2, self.window.height + 150, width = 200, height = 100, function = lambda x = 1: self.start(x))
        button.set_gradient((250, 230, 200), (200, 210, 150), (False, True, True))
        button.set_text('Легкая', (255, 255, 255), 35)
        button.move(self.window.width / 2, self.window.height / 2 - 50, 3)
        self.labels.append(button)

        button = Button(self.window.width / 2, self.window.height + 150, width = 200, height = 100, function = lambda x = 2: self.start(x))
        button.set_gradient((250, 230, 200), (200, 210, 150), (False, True, False))
        button.set_text('Нормальная', (255, 255, 255), 31)
        button.move(self.window.width / 2, self.window.height / 2 + 70, 3)
        self.labels.append(button)

        button = Button(self.window.width / 2, self.window.height + 150, width = 200, height = 100, function = lambda x = 3: self.start(x))
        button.set_gradient((250, 230, 200), (200, 210, 150), (False, False, True))
        button.set_text('Сложная', (255, 255, 255), 35)
        button.move(self.window.width / 2, self.window.height / 2 + 190, 3)
        self.labels.append(button)

    def yes(self):
        self.change_page()

    def no(self):
        self.clear()
        Quizscreen.page = 0
        Quizscreen.quest = None
        Quizscreen.correct = 0

        self.show()

    def start(self, dif):
        Quizscreen.page = 0
        Quizscreen.quest = deepcopy(self.window.quest)
        random.shuffle(Quizscreen.quest)

        if dif == 1:
            for i in range(10):
                Quizscreen.quest[i][1] = [Quizscreen.quest[i][1][0], Quizscreen.quest[i][1][1]]
            Quizscreen.quest = Quizscreen.quest[:10]
        elif dif == 2:
            Quizscreen.quest = Quizscreen.quest[:10]
        elif dif == 3:
            Quizscreen.quest = Quizscreen.quest[:20]

        self.change_page()

    def clear(self):
        for label in self.labels:
            label.remove(-self.window.width / 2, label.position.y, 3)
            label.active = False

    def change_page(self):
        self.clear()

        font = pygame.font.SysFont('Comic Sans MS', 30)

        label = Label(self.window.width / 2, -150)
        label.fill((0, 0, 0, 0))
        label.set_text(Utils.cut_text(Quizscreen.quest[Quizscreen.page][0], font, self.window.width - 250, self.window.height / 2 - 80), (255, 235, 225), 30)
        label.move(self.window.width / 2, self.window.height / 4, 3)
        self.labels.append(label)

        label = Label(self.window.width / 2, self.window.height + 150)
        label.fill((0, 0, 0, 0))
        label.set_text('%i/%i' % (Quizscreen.page + 1, len(Quizscreen.quest)), (255, 235, 225), 30)
        label.move(self.window.width / 2, self.window.height - 50, 3)
        self.labels.append(label)

        pos = random.sample(range(len(Quizscreen.quest[Quizscreen.page][1])), len(Quizscreen.quest[Quizscreen.page][1]))

        for i in range(len(Quizscreen.quest[Quizscreen.page][1])):
            text = Quizscreen.quest[Quizscreen.page][1][i]
            button = Button(self.window.width / 2, self.window.height + 150, width = self.window.width - 100, height = 70, function = lambda x = (i == 0): self.answer(x))
            button.set_gradient((250, 230, 200), (200, 210, 150), (False, False, True))
            button.set_text(text, (255, 255, 255), 25)
            button.move(self.window.width / 2, self.window.height / 2 + 40 + 100 * pos[i], 3)
            self.labels.append(button)

    def answer(self, correct):
        self.clear()

        if correct:
            Quizscreen.correct += 1

        label = Label(self.window.width * 1.5, self.window.height / 2 + 80, width = self.window.width - 100, height = 70)
        if correct:
            label.set_gradient((220, 250, 200), (180, 220, 150), (False, False, True))
        else:
            label.set_gradient((250, 220, 200), (220, 180, 150), (False, False, True))
        label.set_text(Quizscreen.quest[Quizscreen.page][1][0], (255, 255, 255), 30)
        label.move(self.window.width / 2, self.window.height / 2 + 80, 3)
        self.labels.append(label)

        label = Label(self.window.width * 1.5, self.window.height / 2 - 200)
        if correct:
            label.set_image(self.window.images['correct'])
        else:
            label.set_image(self.window.images['incorrect'])
        label.move(self.window.width / 2, self.window.height / 2 - 200, 3)
        self.labels.append(label)

        Quizscreen.page += 1
        Thread(target = self.change_delay, daemon = True).start()

    def change_delay(self):
        was = self.window.screen_number
        time.sleep(2)

        if was == self.window.screen_number:
            if Quizscreen.page < len(Quizscreen.quest):
                self.change_page()
            else:
                self.clear()
                self.results()

    def results(self):
        label = Label(self.window.width / 2, -150)
        label.fill((0, 0, 0, 0))
        label.set_text('Ваш результат:', (255, 255, 255), 35)
        label.move(self.window.width / 2, self.window.height / 2 - 150, 3)
        self.labels.append(label)

        label = Label(self.window.width / 2, -150)
        label.fill((0, 0, 0, 0))
        label.set_text('%i/%i' % (Quizscreen.correct, len(Quizscreen.quest)), (255, 255, 255), 50)
        label.move(self.window.width / 2, self.window.height / 2 - 80, 3)
        self.labels.append(label)

        button = Button(self.window.width / 2, self.window.height + 150, width = 200, height = 100, function = self.save)
        button.set_gradient((250, 230, 200), (200, 210, 150), (False, True, False))
        button.set_text('Сохранить', (255, 255, 255), 31)
        button.move(self.window.width / 2, self.window.height / 2 + 150, 3)
        self.labels.append(button)

        Quizscreen.page = 0
        Quizscreen.quest = None
        Quizscreen.correct = 0

    def save(self):
        file = filedialog.asksaveasfilename(title = 'Выберите место сохранения', filetypes = [('PNG Image', '*.png')])

        if file != '':
            pygame.image.save(Singleton.win, file.replace('.png', '') + '.png')

            self.labels[-1].set_gradient((200, 250, 170), (170, 220, 130), (False, True, False))
            self.labels[-1].set_text('Сохранено!', (235, 255, 215), 31)
            self.labels[-1].active = False

    def back(self):
        self.window.change(screens.Mainscreen())
