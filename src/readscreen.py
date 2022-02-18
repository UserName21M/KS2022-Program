from drawengine import *
import catalog

class Readscreen:
    def __init__(self, tale):
        self.window = Singleton.window
        self.parser = Singleton.parser
        self.color = [Color(220, 130, 180), Color(250, 200, 230)]

        self.font = pygame.font.SysFont('Comic Sans MS', 15)

        self.page = 0
        self.page_label = None
        self.tale = tale
        self.text = self.load_tale()

        self.toshow = [(self.show, 0.5)]
        self.labels = []

        self.favor_button = None

    def show(self):
        if self.text == None:
            self.show_load()
        self.configure_tale()

        button = Button(50, self.window.height + 50, width = 100, height = 50, function = self.back)
        button.set_gradient((220, 130, 180), (250, 200, 230), (False, True, True))
        button.set_text('Вернуться', (255, 255, 255), 16)
        button.move(75, self.window.height - 50, 3)

        self.page_label = Label(self.window.width / 2, self.window.height + 50, width = 50, height = 50)
        self.page_label.fill((0, 0, 0, 0))
        self.page_label.move(self.window.width / 2, self.window.height - 50, 3)

        button = Button(self.window.width / 2, self.window.height + 50, width = 100, height = 50, function = self.next)
        button.set_image(pygame.transform.scale(self.window.images['arrow_right'].copy(), (25, 50)))
        button.image.set_alpha(200)
        button.update_image()
        button.move(self.window.width / 2 + 50, self.window.height - 50, 3)

        button = Button(self.window.width / 2, self.window.height + 50, width = 100, height = 50, function = self.prev)
        button.set_image(pygame.transform.scale(self.window.images['arrow_left'].copy(), (25, 50)))
        button.image.set_alpha(200)
        button.update_image()
        button.move(self.window.width / 2 - 50, self.window.height - 50, 3)

        self.favor_button = Button(self.window.width + 50, self.window.height + 50, width = 100, height = 50, function = self.add_favourite)
        self.favor_button.set_gradient((220, 130, 180), (250, 200, 230), (True, True, False))
        self.favor_button.move(self.window.width - 75, self.window.height - 50, 3)
        self.configure()

        self.change_page()

    def add_favourite(self):
        self.window.favourite.append(self.tale['title'])
        self.window.save_favourite()
        self.configure()

    def remove_favourite(self):
        self.window.favourite.remove(self.tale['title'])
        self.window.save_favourite()
        self.configure()

    def configure(self):
        if self.tale['title'] in self.window.favourite:
            self.favor_button.set_text('Удалить из\nизбранного *', (255, 255, 255), 12)
            self.favor_button.function = self.remove_favourite
        else:
            self.favor_button.set_text('Добавить в\nизбранное *', (255, 255, 255), 12)
            self.favor_button.function = self.add_favourite

    def next(self):
        if self.page == len(self.pages) - 1:
            return

        self.page += 1
        self.change_page(-1)

    def prev(self):
        if self.page == 0:
            return

        self.page -= 1
        self.change_page(1)

    def back(self):
        self.window.change(catalog.Catalog(True))

    def change_page(self, dir = -1):
        for label in self.labels:
            label.remove(label.position.x + self.window.width * dir * 2, label.position.y, 3, True)

        self.page_label.set_text('%i/%i' % (self.page + 1, len(self.pages)), (0, 0, 0), 15)

        for part in self.pages[self.page]:
            label = Label(part[1][0] - self.window.width * dir, part[1][1], self.window.width, 30)
            if part[2] == 1:
                label.fill((0, 0, 0, 10))
                if self.page == 0 and part is self.pages[self.page][0]:
                    label.set_text(part[0], (0, 0, 0), 20)
                else:
                    label.set_text(part[0], (50, 50, 50), 15)
                label.move(part[1][0] - self.window.width / 2 + 30 + label.text_image.get_width() / 2, part[1][1], 3, True)
            elif part[2] == 2:
                label.set_image(part[0])
                label.move(part[1][0], part[1][1], 3, True)
            self.labels.append(label)

    def show_load(self):
        label = Label(self.window.width / 2, -100, width = self.window.width, height = 40)
        label.set_gradient((180, 110, 150), (255, 170, 220), (True, True, True))
        label.set_text('Загружаем сказку', (50, 50, 50), 20)
        label.move(self.window.width / 2, self.window.height / 2, 6, True)

        self.text = self.parser.tale(self.tale['link'])
        self.text['images'] = self.parser.download_images(self.text['image_links'], save_size = True)
        self.parser.save_file(self.text, 'data/saves/' + self.tale['title'])

        label.remove(self.window.width / 2, self.window.height + 100, 3, True)

    def configure_tale(self):
        for i in range(len(self.text['images'])):
            self.text['images'][i] = pygame.image.fromstring(self.text['images'][i][0], self.text['images'][i][1], 'RGB').convert()
            self.text['images'][i] = Utils.add_frame(self.text['images'][i], (160, 110, 250), 20)

        index = 0
        while index < len(self.text['text']) - 1:
            text = self.text['text'][index]
            text1 = self.text['text'][index + 1]

            if text[:4] != 'img_' and text1[:4] != 'img_':
                self.text['text'].pop(index)
                self.text['text'].pop(index)
                self.text['text'].insert(index, text + text1)
            else:
                index += 2

        _text = []
        for part in self.text['text']:
            if part[:4] == 'img_':
                _text.append(part)
            else:
                for line in part.split('\n'):
                    line = Utils.cut_text(line, self.font, self.window.width - 150, self.window.height - 100, False)
                    for a in line.split('\n'):
                        _text.append(a)
        self.text['text'] = _text

        self.pages = []

        size = self.font.size(self.tale['title'])
        self.pages.append([(self.tale['title'], (self.window.width / 2, 30 + size[1] / 2), 1)])
        y = 30 + size[1] + 10

        if self.text['author'] != None:
            size = self.font.size(self.text['author'])
            self.pages[-1].append((self.text['author'], (self.window.width / 2, y + size[1] / 2), 1))
            y += size[1] + 10
        y += 10

        index, next, height = 0, None, 0
        while True:
            if next == None:
                if index == len(self.text['text']):
                    break
                part = self.text['text'][index]
                index += 1
                if part == '':
                    continue

                if part[:4] == 'img_':
                    part = self.text['images'][int(part[4:])].copy()
                    height = part.get_height()
                else:
                    height = self.font.size(part)[1]
            else:
                part = next
                next = None

            if y + height > self.window.height - 100:
                if type(part) is str:
                    next = part
                else:
                    h = self.window.height - y - 100
                    if h < 150:
                        next = part
                    else:
                        self.pages[-1].append((pygame.transform.scale(part, (int(part.get_width() * h / height), h)), (self.window.width / 2, y + h / 2), 2))
                y = 30
                self.pages.append([])
            else:
                if type(part) is str:
                    self.pages[-1].append((part, (self.window.width / 2, y + height / 2), 1))
                    y += height + 10
                else:
                    self.pages[-1].append((part, (self.window.width / 2, y + height / 2), 2))
                    y += height + 10

    def load_tale(self):
        try:
            return self.parser.load_file('data/saves/' + self.tale['title'])
        except:
            return None
