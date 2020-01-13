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


from settings import category_urls
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