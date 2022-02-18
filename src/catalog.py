from drawengine import *
from readscreen import *
import screens

class Catalog:
    last_tale = 0
    search_text = ''

    def __init__(self, to_overview = False):
        self.window = Singleton.window
        self.color = [Color(200, 80, 80), Color(250, 180, 180)]

        self.toshow = [(self.show, 0.5), (self.show_delay, 1), (self.input_loop, 0.75)]
        self.labels = {}

        self.to_overview = to_overview
        self.catalog = self.get_catalog()

        if type(Catalog.last_tale) is not int:
            Catalog.last_tale = self.catalog.index(Catalog.last_tale)

    def show(self):
        self.labels['search'] = Label(185, -100, width = self.window.width - 130, height = 40)
        self.labels['search'].fill((240, 240, 240))
        self.labels['search'].update_image()

        if Catalog.search_text == '':
            self.labels['search'].set_text('Начните ввод с клавиатуры для поиска', (15, 15, 15), 15) # 'Поиск Entry'
        else:
            self.labels['search'].set_text(Catalog.search_text, (15, 15, 15), 15)

        self.labels['favourite'] = Button(self.window.width - 60, -100, width = 100, height = 40, function = self.favourite)
        self.labels['favourite'].set_gradient((250, 200, 200), (200, 160, 150), (False, True, True))
        self.labels['favourite'].set_text('Избранное *', (255, 255, 255), 15)

        self.labels['arrow_left'] = Button(-100, self.window.height / 2, width = 200, height = 400, function = self.prev)
        self.labels['arrow_left'].set_image(self.window.images['arrow_left'])

        self.labels['arrow_right'] = Button(self.window.width + 100, self.window.height / 2, width = 200, height = 400, function = self.next)
        self.labels['arrow_right'].set_image(self.window.images['arrow_right'])

        delta = self.catalog[Catalog.last_tale]['img'].get_height() / 2

        self.labels['clock'] = Label(self.window.width - 10, self.window.height + 100)
        self.labels['clock'].set_image(self.window.images['clock'])

        self.labels['tale'] = Button(self.window.width + 200, self.window.height / 2, width = 300, height = 600)
        self.configure_tale()

        self.labels['time'] = Label(self.window.width + 50, self.window.height + 100, width = 100, height = 30)
        self.labels['time'].fill((0, 0, 0, 0))
        self.labels['time'].set_text(self.catalog[Catalog.last_tale]['time'], (0, 0, 0), 15)

        self.labels['title'] = Label(-self.window.width / 2, 180, width = 100, height = 30)
        self.labels['title'].fill((0, 0, 0, 0))
        self.labels['title'].set_text(self.catalog[Catalog.last_tale]['title'], (50, 0, 0), 30 - int(len(self.catalog[Catalog.last_tale]['title']) / 4))

        self.labels['back'] = Button(50, self.window.height + 50, width = 100, height = 50, function = self.back)
        self.labels['back'].set_gradient((250, 200, 200), (200, 160, 160), (False, True, True))
        self.labels['back'].set_text('Назад', (255, 255, 255), 20)

        self.labels['desc'] = Label(self.window.width / 2, self.window.height * 1.5, width = 450, height = 350)
        self.labels['desc'].set_text(' ', (0, 0, 0), 18)
        self.labels['desc'].fill((0, 0, 0, 50))

        self.labels['read'] = Button(312.5, self.window.height * 1.5, width = 325, height = 50, function = self.read)
        self.labels['read'].set_gradient((200, 200, 250), (160, 160, 200), (False, True, True))
        self.labels['read'].set_text('Читать', (255, 255, 255), 20)

        self.start_move()
        if self.to_overview:
            self.show_delay(False)
            self.overview()

    def show_delay(self, check = True):
        if self.to_overview and check:
            return

        self.labels['list'] = Button(-self.window.width / 2, 80, width = self.window.width - 20, height = 40, function = self.tolist)
        self.labels['list'].set_gradient((250, 200, 200), (200, 110, 160), (False, True, True))
        self.labels['list'].set_text('Список сказок', (255, 255, 255), 15)
        self.labels['list'].move(self.window.width / 2, 80, 3, True)

    def input_loop(self):
        num = self.window.screen_number
        while num == self.window.screen_number:
            pressed = []
            was = Singleton.input.last_events

            for e in was:
                if e.type == pygame.KEYDOWN:
                    pressed.append(e.unicode)

            wastext = Catalog.search_text
            for char in pressed:
                if char == '\x08':
                    Catalog.search_text = Catalog.search_text[:-1]
                elif len(Catalog.search_text) < 40:
                    Catalog.search_text += char

            if wastext != Catalog.search_text:
                self.labels['search'].set_text(Catalog.search_text, (15, 15, 15), 15)
                if self.catalog:
                    wastale = self.catalog[Catalog.last_tale]

                self.catalog = self.get_catalog()

                if self.catalog and wastale != self.catalog[0]:
                    Catalog.last_tale = -1
                    self.next()

            while was is Singleton.input.last_events:
                time.sleep(0.01)

    def get_catalog(self):
        return [i for i in self.window.catalog if Catalog.search_text.lower() in i['title'].lower()]

    def favourite(self):
        self.window.change(Listscreen([i for i in self.window.catalog if i['title'] in self.window.favourite]))

    def next(self):
        if Catalog.last_tale == len(self.catalog) - 1:
            return
        Catalog.last_tale += 1

        self.labels['tale'].active = False
        self.labels['tale'].remove(-200, self.window.height / 2, 3)

        self.labels['tale'] = Button(self.window.width + 200, self.window.height / 2, width = 300, height = 600)
        self.labels['tale'].move(self.window.width / 2, self.window.height / 2, 3, False)
        self.configure_tale()

    def prev(self):
        if Catalog.last_tale <= 0:
            return
        Catalog.last_tale -= 1

        self.labels['tale'].active = False
        self.labels['tale'].remove(self.window.width + 200, self.window.height / 2, 3)

        self.labels['tale'] = Button(-200, self.window.height / 2, width = 300, height = 600)
        self.labels['tale'].move(self.window.width / 2, self.window.height / 2, 3, False)
        self.configure_tale()

    def configure_tale(self):
        tale = self.catalog[Catalog.last_tale]

        delta = tale['img'].get_height() / 2

        _tale = self.labels['tale']
        image = Utils.add_frame(tale['img'], (200, 75, 75), 20)
        _tale.set_image(image)
        _tale.active = False
        _tale.activate_after = True
        _tale.function = self.overview

        if 'time' in self.labels:
            _time = self.labels['time']
            _time.remove(_time.position.x, _time.position.y + 35, 20, True)
            _time.fade = -1

            _time = Label(self.window.width / 2 + 50, self.window.height / 2 + delta + 30, width = 100, height = 30)
            _time.fill((0, 0, 0, 0))
            _time.move(self.window.width / 2 + 10, self.window.height / 2 + delta + 30, 4, False)
            _time.fade = 1
            self.labels['time'] = _time

            _time.set_text(tale['time'], (0, 0, 0), 15)

            self.labels['clock'].move(self.window.width / 2 - 40, self.window.height / 2 + delta + 30, 2, False)

        if 'title' in self.labels:
            _title = self.labels['title']
            _title.remove(_title.position.x, _title.position.y - 35, 20, True)
            _title.fade = -1

            _title = Label(self.window.width / 2, self.window.height / 2 - delta - 75, width = 100, height = 30)
            _title.fill((0, 0, 0, 0))
            _title.move(self.window.width / 2, self.window.height / 2 - delta - 40, 4, False)
            _title.fade = 1
            self.labels['title'] = _title

            _title.set_text(tale['title'], (50, 0, 0), 30 - int(len(tale['title']) / 4))

    def back(self):
        self.window.change(screens.Mainscreen())

    def tolist(self):
        self.window.change(Listscreen(self.catalog))

    def overview(self):
        self.labels['search'].move(self.labels['search'].rect.width / 2 + 10, -80, 3, True)
        self.labels['favourite'].move(self.window.width - 60, -80, 3, True)
        self.labels['list'].move(-self.window.width / 2 - 200, 80, 5, True)
        self.labels['arrow_left'].move(-40, self.window.height / 2, 3, True)
        self.labels['arrow_right'].move(self.window.width + 40, self.window.height / 2, 3, True)

        self.labels['back'].set_gradient((250, 200, 210), (200, 140, 160), (False, True, True))
        self.labels['back'].function = self.back_overview

        _title = self.labels['title']
        _title.move(self.window.width / 2, 20 + _title.text_image.get_height() / 2, 3, False)

        _tale = self.labels['tale']
        tale_y = 40 + _tale.rect.height / 2 + _title.text_image.get_height()
        _tale.move(20 + _tale.rect.width / 2, tale_y, 3, False)

        self.labels['clock'].move(410, tale_y - 30, 3, False)
        self.labels['time'].move(410, tale_y + 30, 3, False)

        desc_height = self.window.height - _title.text_image.get_height() - 160 - _tale.rect.height
        _desc = self.labels['desc']
        _desc.resize(_desc.rect.width, desc_height)
        _desc.move(self.window.width / 2, self.window.height - 100 - desc_height / 2, 3, False)
        self.labels['read'].move(312.5, self.window.height - 50, 3, False)

        _desc.set_text(Utils.cut_text(self.catalog[Catalog.last_tale]['desc'], _desc.font, 250, desc_height - 50), (255, 230, 230), 18)

        todisable = ['arrow_left', 'arrow_right', 'list', 'search', 'favourite', 'tale']
        for label in self.labels:
            if label in todisable:
                self.labels[label].active = False

    def back_overview(self):
        self.start_move()

        self.labels['back'].set_gradient((250, 200, 200), (200, 160, 160), (False, True, True))
        self.labels['back'].function = self.back

        toactivate = ['arrow_left', 'arrow_right', 'list', 'search', 'favourite', 'tale']
        for label in self.labels:
            if label in toactivate:
                self.labels[label].active = True

    def start_move(self):
        self.labels['search'].move(self.labels['search'].rect.width / 2 + 10, 30, 3, True)
        self.labels['favourite'].move(self.window.width - 60, 30, 3, False)
        self.labels['arrow_left'].move(40, self.window.height / 2, 3, False)
        self.labels['arrow_right'].move(self.window.width - 40, self.window.height / 2, 3, False)
        self.labels['back'].move(75, self.window.height - 50, 3)
        if 'list' in self.labels:
            self.labels['list'].move(self.window.width / 2, 80, 3, True)

        delta = self.catalog[Catalog.last_tale]['img'].get_height() / 2
        self.labels['clock'].move(self.window.width / 2 - 40, self.window.height / 2 + delta + 30, 3, False)
        self.labels['tale'].move(self.window.width / 2, self.window.height / 2, 3, False)
        self.labels['time'].move(self.window.width / 2 + 10, self.window.height / 2 + delta + 30, 3, False)
        self.labels['title'].move(self.window.width / 2, self.window.height / 2 - delta - 40, 3, False)

        self.labels['desc'].move(self.window.width / 2, self.window.height * 1.5, 3, False)
        self.labels['read'].move(312.5, self.window.height + 100, 3, False)

    def read(self):
        self.window.change(Readscreen(self.catalog[Catalog.last_tale]))

class Listscreen:
    def __init__(self, tales = None):
        self.window = Singleton.window
        self.color = [Color(200, 120, 120), Color(250, 200, 200)]

        self.toshow = [(self.show, 0.5)]
        self.labels = []

        if tales == None:
            self.catalog = self.window.catalog
        else:
            self.catalog = tales

        self.page = 0
        self.onpage = int((self.window.height - 200) / 30)

    def show(self):
        button = Button(50, self.window.height + 50, width = 100, height = 50, function = self.back)
        button.set_gradient((250, 150, 150), (200, 110, 110), (False, True, True))
        button.set_text('Назад', (255, 255, 255), 20)
        button.move(75, self.window.height - 50, 3)

        button = Button(self.window.width / 2, -50, width = 100, height = 50, function = self.prev)
        button.set_image(pygame.transform.scale(self.window.images['arrow_up'].copy(), (200, 50)))
        button.image.set_alpha(30)
        button.update_image()
        button.move(self.window.width / 2, 50, 3)

        button = Button(self.window.width / 2, self.window.height + 50, width = 100, height = 50, function = self.next)
        button.set_image(pygame.transform.scale(self.window.images['arrow_down'].copy(), (200, 50)))
        button.image.set_alpha(30)
        button.update_image()
        button.move(self.window.width / 2, self.window.height - 50, 3)

        self.change_page()

    def change_page(self, dir = 1):
        for label in self.labels:
            label.remove(self.window.width / 2, label.position.y + self.window.height * dir, 3, True)

        self.labels = []
        for i in range(self.onpage):
            if self.page * self.onpage + i >= len(self.catalog):
                break

            tale = self.catalog[self.page * self.onpage + i]
            button = Button(self.window.width / 2, 100 + i * 30 - self.window.height * dir, self.window.width * 0.8, 30, function = lambda x = tale: self.choose(x))
            button.set_text(tale['title'], (0, 0, 0), 15 - len(tale['title']) // 15)
            button.fill((0, 0, 0, 20 * (i % 2)))
            button.update_image()
            button.move(self.window.width / 2, 100 + i * 30, 3, True)

            self.labels.append(button)

    def choose(self, tale):
        Catalog.last_tale = tale
        self.window.change(Catalog(True))

    def back(self):
        self.window.change(Catalog())

    def next(self):
        if self.page >= len(self.catalog) / self.onpage - 1:
            return
        self.page += 1
        self.change_page(-1)

    def prev(self):
        if self.page == 0:
            return
        self.page -= 1
        self.change_page(1)
