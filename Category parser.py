import requests

from threading import Thread

from bs4 import BeautifulSoup as bs

from random import randint

import time


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
            print(f'Error...( {url}')

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

    pages_statuses = [False for i in range(number_of_pages)]
    for page_number in range(1, number_of_pages + 1):
        page_url = f'{url}?page={page_number}'
        
        print(page_url)
        
        thread = Thread(target = parse_page, args = (page_url, page_number - 1))
        thread.start()
        
        time.sleep(0.1)

    while False in pages_statuses:
        time.sleep(1)

    categories_statuses[category_index] = True


with open('Perfect proxy list.txt', 'r', encoding = 'UTF-8') as file:
    good_proxies = [{
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    } for proxy in file.read().split('\n')]


category_urls = {
    'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/kha/q-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%BC-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%83/': ['Харьков', 209],
    'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/ko/q-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%BC-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%83/': ['Киев', 169],
    'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/od/q-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%BC-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%83/': ['Одесса', 210],
    'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/dnp/q-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%BC-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%83/': ['Днепр', 140],
    'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/don/q-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%BC-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%83/': ['Донецк', 100],
    'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/zap/q-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%BC-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%83/': ['Запорожье', 50],
    'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/lv/q-%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%BC-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%83/': ['Львов', 20]
}
unsuccess_urls = {}
all_links_list = []
categories_statuses = [False for i in category_urls]
for index, category_url in enumerate(category_urls):
	thread = Thread(target = parse_category,
		            args = (category_url, category_urls[category_url][0], category_urls[category_url][1], index,))
	thread.start()
	time.sleep(1)
    #parse_category(category_url, category_urls[category_url][0], category_urls[category_url][1], index)
    #break

while False in categories_statuses:
	time.sleep(1)
	print('iuhfiughighghrghtrihg')

with open('Links.txt', 'w', encoding = 'UTF-8') as file:
    file.write('\n'.join(all_links_list))