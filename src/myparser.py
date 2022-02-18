from bs4 import BeautifulSoup as bs
from threading import Thread
import urllib3
import json

import pickle
import bz2
import os

import pygame
import io

class Parser:
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.data = []
        self.progress = 0

    def catalog(self, page):
        payload = {'page': page, 'sort': 'date', 'tags': 1, 'category': 1, 'img': 0, 'dmin': 0, 'dmax': 0, 'subtype': 'tale'}
        resp = self.http.request('POST', 'https://nukadeti.ru/ajax/tale/get_tales', fields = payload)

        html = json.loads(resp.data)
        self.catalog_parse(html)

    def catalog_parse(self, html):
        soup = bs(html['html'], 'lxml')
        lis = soup.find_all('li', class_ = 'st-bl')
        for li in lis:
            title = li.find('a', class_ = 'title')
            link = title['href']
            title = title.text

            img = li.find('img')
            try:
                img = img['src']
            except KeyError:
                img = img['data-src']

            desc = li.find('div', class_ = 'desc')
            if desc != None:
                desc = desc.text
            else:
                desc = 'Без описания'
            time = li.find('div', class_ = 'it dur').text.replace('Время чтения: ', '')
            tags = [a.text for a in li.find('div', class_ = 'tags').find_all('a')]

            self.data.append({'title': title, 'img_link': img.replace('300x300', '400x400'), 'desc': desc, 'time': time, 'tags': tags, 'link': link, 'img': [None, None]})

    def tale(self, link):
        resp = self.http.request('POST', 'https://nukadeti.ru' + link)
        return self.tale_parse(resp.data)

    def tale_parse(self, html):
        soup = bs(html, 'lxml')

        desc = soup.find('div', class_ = 'cont si-text')
        if desc != None:
            desc = desc.text
        else:
            desc = 'Без описания'

        text = []
        image_links = []

        author = soup.find('a', class_ = 'aut')
        if author != None:
            author = author.text

        tale = soup.find('div', class_ = 'tale-text si-text')
        tale = tale.find_all('p')
        for part in tale:
            img = part.find('img')
            if img != None:
                text.append('img_%i' % len(image_links))
                image_links.append(img['src'])
            else:
                text.append('        ' + part.text.replace('\r', '') + '\n')

        full = {'text': text, 'image_links': image_links, 'images': [], 'author': author}
        return full

    def download_images(self, images, width = 300, save_size = False):
        self.progress = 0
        if not save_size:
            tolist = [None] * len(images)
        else:
            tolist = []
            for i in range(len(images)):
                tolist.append([None, None])
#            tolist = [[None, None]] * len(images)

        threads = []
        for i in range(len(images)):
            threads.append(Thread(target = self.download_image, args = (images[i], tolist, i, width, save_size)))
            threads[-1].start()

        for thread in threads:
            thread.join()
            self.progress += 1 / len(images)

        return tolist

    def download_image(self, link, tolist, i, width = 300, save_size = False):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

        data = self.http.request('GET', 'https://nukadeti.ru' + link, headers = headers).data

        image = io.BytesIO(data)
        image = pygame.image.load(image)

        scale = width / image.get_width()
        size = (width, int(image.get_height() * scale))
        image = pygame.transform.scale(image, size)

        if save_size:
            tolist[i][1] = size
            tolist[i][0] = pygame.image.tostring(image, 'RGB')
        else:
            tolist[i] = pygame.image.tostring(image, 'RGB')

    def update(self, pages = 10):
        self.progress = 0

        threads = []
        for i in range(1, pages + 1):
            threads.append(Thread(target = self.catalog, args = (i, ), daemon = True))
            threads[-1].start()

        for thread in threads:
            thread.join()
            self.progress += 1 / pages

        self.progress = 0

        threads = []
        for tale in self.data:
            print(tale['img'])
            threads.append(Thread(target = self.download_image, args = (tale['img_link'], [tale['img']], 0, 300, True), daemon = True))
            threads[-1].start()

        for thread in threads:
            thread.join()
            self.progress += 1 / len(self.data) * 0.8

        self.save_file(self.data, 'data/data')
        self.progress = 1

        return self.data

    def save_file(self, data, file):
        folders = file.split('/')[:-1]
        path = ''

        for folder in folders:
            path += folder + '/'
            if not os.path.exists(path):
                os.mkdir(path)

        file = bz2.BZ2File(file, 'w')
        pickle.dump(data, file)
        file.close()

    def load_file(self, file):
        file = bz2.BZ2File(file, 'rb')
        print('loading')
        data = pickle.load(file)
        print('done')
        file.close()

        return data
