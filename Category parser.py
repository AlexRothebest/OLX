import sys

import requests

from threading import Thread, Event

from bs4 import BeautifulSoup as bs

from random import randint

import time

from tkinter import *


class StoppableThread(Thread):
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def create_thread(function, args = ()):
    global all_threads

    print('Thread created')

    while True:
        try:
            thread = StoppableThread(target = function, args = args)
            thread.start()
            all_threads.append(thread)
            break
        except Exception as e:
            raise e

            time.sleep(3)


def get_html(url):
    global good_proxies

    while True:
        try:
            proxies = good_proxies[randint(0, len(good_proxies) - 1)]

            response_local = requests.get(url, proxies = proxies, timeout = 5)
            if response_local.status_code == 200:
                response = response_local
                break
        except:
        	#pass
            print(f'Error... {url}')

    return response.text


def parse_category(url, city, number_of_pages, category_index):
    global categories_statuses

    def parse_page(url, page_index):
        global all_links_list
        nonlocal pages_statuses, city

        html = get_html(url)

        soup = bs(html, 'html.parser')

        urls_list = []
        for a in soup.find_all('a', class_ = 'detailsLink'):
            if 'marginright5' in  a.attrs['class']:
                urls_list.append(a.get('href'))

        if len(urls_list) != 44:
            unsuccess_urls[url] = len(urls_list)

        for url in urls_list:
            if url not in all_links_list:
                all_links_list.append(f'{url}-{city}')
                print(f'{url}-{city}')

        pages_statuses[page_index] = True

    #number_of_pages = 1############################################################################

    pages_statuses = [False for i in range(number_of_pages)]
    for page_number in range(1, number_of_pages + 1):
        if '?' in url:
            page_url = f'{url}&page={page_number}'
        else:
            page_url = f'{url}?page={page_number}'
        
        print(page_url)

        if page_url.strip() == '':
            print('$' * 1000)
            continue
        
        thread = Thread(target = parse_page, args = (page_url, page_number - 1))
        thread.start()
        
        time.sleep(0.1)

    while False in pages_statuses:
        time.sleep(1)

    categories_statuses[category_index] = True


def write_info(event = None):
    global all_links_list

    with open('Links.txt', 'w', encoding = 'UTF-8') as file:
        file.write('\n'.join(all_links_list))


def parse(event = None):
    global category_urls, unsuccess_urls, all_links_list, categories_statuses

    for index, category_url in enumerate(category_urls):
        create_thread(parse_category,
                      (category_url, category_urls[category_url][0], category_urls[category_url][1], index,))
        # thread = Thread(target = parse_category,
        #                 args = (category_url, category_urls[category_url][0], category_urls[category_url][1], index,))
        # thread.start()
        time.sleep(1)
        #parse_category(category_url, category_urls[category_url][0], category_urls[category_url][1], index)
        #break


def create_interface():
    global root

    root = Tk()
    root.title('OLX category parser')
    root.minsize(260, 110)

    save_button = Button(root, text = 'Занести уже собранные\nданные в файл', width = 25, height = 2)
    save_button.bind('<Button-1>', lambda event: create_thread(write_info, ()))
    save_button.place(x = 40, y = 30)

    root.mainloop()


with open('Perfect proxy list.txt', 'r', encoding = 'UTF-8') as file:
    good_proxies = [{
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    } for proxy in file.read().split('\n')]


from settings import category_urls
unsuccess_urls = {}
all_links_list = []
categories_statuses = [False for i in category_urls]   


all_threads = []

create_thread(create_interface)

create_thread(parse)


while False in categories_statuses:
	time.sleep(1)
	print('iuhfiughighghrghtrihg')

create_thread(root.destroy)

print('ewkljfeiljfeikljfreterikoljgt')

write_info()

print('ewkljfeiljfeikljfreterikoljgt (2)')

for thread in all_threads:
    pass
    # thread.stop()

sys.exit()