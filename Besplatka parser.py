import os

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

import requests

from bs4 import BeautifulSoup as bs

import sqlite3

from datetime import datetime

import time

from random import randint

from threading import Thread


def write_sql(data):
    open('data.sqlite3', 'w')

    db = sqlite3.connect('data.sqlite3')
    cursor = db.cursor()

    '''
    cursor.execute('SELECT * FROM places')
    for row in cursor.fetchall():
        print(row)

    time.sleep(30)
    '''

    cursor.execute('CREATE TABLE IF NOT EXISTS places (id INTEGER PRIMARY KEY,\
    title TEXT, description TEXT, category VARCHAR(255), name VARCHAR(255), price VARCHAR(255), currency VARCHAR(255),\
    city VARCHAR(255), countryId VARCHAR(255), country VARCHAR(255), phone VARCHAR(255),\
    images VARCHAR(255), datetime VARCHAR(255), customs TEXT)')
    cols = ['title', 'description ', 'category', 'name', 'price', 'currency',\
            'city', 'countryId', 'country', 'phone', 'images', 'datetime', 'customs']

    data = [f"({str(['kljgkgfkfhgfjhgfh' for i in range(len(cols))])[1: -1]})" for i in range(10)]

    data_str = ',\n'.join(data)

    cursor.execute(f'''
    INSERT INTO places ({', '.join(cols)})
    VALUES {data_str}
    ''')

    cursor.execute('SELECT * FROM places')
    for row in cursor.fetchall():
        print(row)

    db.commit()
    cursor.close()
    db.close()


def get_html(url):
    global good_proxies

    def get_response():
        global good_proxies
        nonlocal response, url

        try:
            proxies = good_proxies[randint(0, len(good_proxies) - 1)]

            response_local = requests.get(url, proxies = proxies)
            if response_local.status_code == 200:
                response = response_local
        except:
            print(f'Error...( {url}')

    response = None
    while response is None:
        #get_response()
        #print(response)
        thread = Thread(target = get_response, args = ())
        thread.start()
        time.sleep(0.5)

    return response.text


def get_html_proxy(url, proxies = {}):
    return requests.get(url, proxies = proxies, timeout = 1).text


def parse_place(driver, url, driver_index):
    global data_list, driver_statuses, drivers

    driver.get(url)
    time.sleep(20)

    if drivers[index].page_source.find('На прокси-сервере возникла проблема или адрес указан неверно') != -1 or\
       drivers[index].page_source.find('Please complete the security check to access besplatka.ua') != -1:
        reload_driver(driver_index)
        driver = drivers[driver_index]

    #driver.get(ip_url)
    #time.sleep(5)
    #print(driver.page_source)
    #driver.execute_script("document.getElementById('contact_methods').getElementsByTagName('strong')[0].click()")
    #driver.execute_script('arguments[0].click()', driver.find_element_by_id('contact_methods').find_element_by_class_name(strong))
    #driver.execute_script('arguments[0].click()', driver.find_element_by_partial_link_text('Показать больше характеристик'))
    driver.execute_script('arguments[0].click()', driver.find_element_by_partial_link_text('Показать'))
    start_time = datetime.now()
    while (datetime.now() - start_time).seconds < 5:
        try:
            phone = driver.execute_script("return document.getElementsByClassName('title-phones')[0].innerText.trim()")
            break
        except:
            time.sleep(0.1)
    title = driver.execute_script("return document.getElementsByClassName('card-title')[0].innerText.trim()")
    description = driver.execute_script("return document.getElementsByClassName('card-description')[0].innerText.trim()")
    category = driver.execute_script("return document.getElementById('message-breadcrumbs').getElementsByTagName('li')")[-1].text.strip()
    name = driver.execute_script("return document.getElementsByClassName('user-name')[0].getElementsByTagName('span')[0].innerText.trim()")
    price = driver.execute_script("return document.getElementsByClassName('card-price')[0].getElementsByTagName('span')[0].innerText.trim()")
    try:
        city = driver.find_element_by_xpath("//span[@itemprop = 'addressLocality']").text.strip()
    except:
        city = ''
    photos = [img.get_attribute('src') for img in driver.execute_script("return document.getElementsByClassName('message-image ms-slider-container')[0].getElementsByTagName('img')")]
    post_datetime = driver.execute_script("return document.getElementsByClassName('list-inline card-info hidden-xs')[0].children[1].innerText.trim()")
    if post_datetime.find(',') != -1:
        post_datetime = post_datetime[:post_datetime.find(',')]
    post_datetime = post_datetime[post_datetime.rfind(' ') + 1:]
    chars = {
        prop_block.find_element_by_class_name('key').get_attribute('innerText').strip():\
        prop_block.find_element_by_class_name('value').get_attribute('innerText').strip()\
        for prop_block in driver.find_elements_by_class_name('property')
    }
    chars_str = ''
    for prop in chars:
        chars_str += f'{prop}:{chars[prop]};'
    print(name)
    print(chars)

    data_list.append({
        'title': title,
        'description ': description,
        'category': category,
        'name': name,
        'price': price,
        'currency': 'грн',
        'city': city,
        'countryId': 'UKR',
        'country': 'Ukraine',
        'phone': phone,
        'images': ';'.join(photos),
        'datetime': post_datetime,
        'customs': chars_str
    })

    driver_statuses[driver_index] = 'free'


def parse_page(url):
    global place_links

    html = get_html(url)
    soup = bs(html, 'html.parser')
    links = ['https://besplatka.ua' + a.get('href') for a in soup.find_all('a', class_ = 'm-title')]
    #print('\n'.join(links))
    for link in links:
        if link not in place_links:
            place_links.append(link)
            print(f'Link: {link}')


def parse_category(category_url):
    global place_links

    number_of_pages = int(bs(get_html(category_url), 'html.parser').find('ul', class_ = 'pagination').find_all('li')[-2].a.text.strip())
    print(f'Number of pages: {number_of_pages}')

    last_links = []
    for page_number in range(1, number_of_pages + 1):
        page_url = f'{category_url}/page/{page_number}'
        thread = Thread(target = parse_page, args = (page_url,))
        thread.start()
        #parse_page(page_url)
        time.sleep(0.1)


'''
    for x in range(20):
        print('-' * 100)
        for i in range(1, 6):
            print(f'Attempt number {i}')
            try:
                number_of_pages = int(bs(get_html(category_url), 'html.parser').find('ul', class_ = 'pagination').find_all('li')[-2].a.text.strip())
                break
            except Exception as e:
                raise e
                number_of_pages = 1
'''


def check_proxy(proxies, proxy):
    global good_proxies, proxy_file

    start_time = datetime.now()
    try:
        html = get_html_proxy('https://icanhazip.com', proxies).strip()
        print(f'\nHTML: {html}\nProxy: {proxy}\nTime: {(datetime.now() - start_time).seconds}\n\n')
        if 0 < len(html) < 25:
            good_proxies.append(proxies)
            #proxy_file.write(f'{proxy} {(datetime.now() - start_time).seconds}\n')
            proxy_file.write(proxy + '\n')
            if randint(1, 3) == 3:
                proxy_file.close()
                proxy_file = open('Proxies list.txt', 'a')
    except:
        pass


def check_all_proxies(proxies_list):
    for proxies in proxies_list:
        proxy = proxies['https'][8:]
        print(proxy)
        thread = Thread(target = check_proxy, args = (proxies, proxy,))
        thread.start()
        time.sleep(0.1)
        #check_proxy(proxies)


def search_awmproxy():
    base_url = 'https://awmproxy.net/freeproxy_b0b6cee28e0e20b.txt'

    proxies_list = [{
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    } for proxy in get_html_proxy(base_url).split('\n')]

    print(f'Proxies found: {len(proxies_list)}\n')

    check_all_proxies(proxies_list)


with open('Links 2.txt', 'r', encoding = 'UTF-8') as file:
    place_links = file.read().split('\n')

with open('Proxies list.txt', 'r') as file:
    proxy_list = file.read().split('\n')


def reload_driver(index):
    global drivers, driver_statuses, proxy_number, ip_url

    print(f'Reloading driver {index}')

    while True:     #drivers[index].page_source.find('На прокси-сервере возникла проблема или адрес указан неверно') != -1:
        drivers[index].quit()

        proxy = proxy_list[proxy_number % len(proxy_list)]
        proxy_number += 1
        print(proxy)

        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.http_proxy = proxy
        prox.https_proxy = proxy
        prox.socks4_proxy = proxy
        prox.ftp_proxy = proxy
        prox.ssl_proxy = proxy
        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)

        options = Options()
        #options.add_argument('--headless')

        driver = Chrome('chromedriver.exe', options = options, desired_capabilities = capabilities)
        driver.get(ip_url)

        drivers[index] = driver

        break

    driver_statuses[index] = 'free'


ip_url = 'https://icanhazip.com'
url = 'https://besplatka.ua'

number_of_drivers = 2
drivers = []
for i in range(number_of_drivers):
    proxy = proxy_list[i]
    print(proxy)

    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = proxy
    prox.https_proxy = proxy
    prox.socks4_proxy = proxy
    prox.ftp_proxy = proxy
    prox.ssl_proxy = proxy
    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    options = Options()
    #options.add_argument('--headless')

    driver = Chrome('chromedriver.exe', options = options, desired_capabilities = capabilities)
    thread = Thread(target = driver.get, args = (ip_url,))
    thread.start()
    #driver.get(ip_url)

    drivers.append(driver)

proxy_number = number_of_drivers
driver_statuses = ['free' for i in range(number_of_drivers)]

data_list = []
for link in place_links:
    while True:
        try:
            index = driver_statuses.index('free')

            if drivers[index].page_source.find('На прокси-сервере возникла проблема или адрес указан неверно') != -1 or\
               drivers[index].page_source.find('Please complete the security check to access besplatka.ua') != -1:
                driver_statuses[index] = 'reloading'

                thread = Thread(target = reload_driver, args = (index,))
                thread.start()

            driver_statuses[index] = 'busy'

            thread = Thread(target = parse_place, args = (drivers[index], link, index,))
            thread.start()
            break
        except:
            pass

'''
proxy_file = open('Proxies list.txt', 'w')

good_proxies = []

#thread = Thread(target = search_awmproxy, args = ())
#thread.start()
search_awmproxy()

time.sleep(10)

proxy_file.close()


print('\nGood proxies:\n' + '\n'.join(proxies['https'][8:] for proxies in good_proxies) + '\n')


category_urls = [
    'https://besplatka.ua/nedvizhimost/arenda-garazhey-i-avtomest',
    'https://besplatka.ua/nedvizhimost/arenda-zemelnih-uchastkov',
    'https://besplatka.ua/nedvizhimost/arenda-kvartiry',
    'https://besplatka.ua/nedvizhimost/arenda-komercheskoy-nedvizhimosti',
    'https://besplatka.ua/nedvizhimost/arenda-komnat',
    'https://besplatka.ua/nedvizhimost/arenda-nedvizhimosti-za-rubezhom',
    'https://besplatka.ua/nedvizhimost/kuplyu',
    'https://besplatka.ua/nedvizhimost/obmen',
    'https://besplatka.ua/nedvizhimost/prodazha-garazhey-i-avtomest',
    'https://besplatka.ua/nedvizhimost/prodazha-domov',
    'https://besplatka.ua/nedvizhimost/prodazha-zemelnih-uchastkov',
    'https://besplatka.ua/nedvizhimost/prodazha-kvartir',
    'https://besplatka.ua/nedvizhimost/prodazha-komercheskoy-nedvizhimosti',
    'https://besplatka.ua/nedvizhimost/prodazha-komnat',
    'https://besplatka.ua/nedvizhimost/prodazha-nedvizhimosti-za-rubezhom',
    'https://besplatka.ua/nedvizhimost/snimu'
]

place_links = []
for category_url in category_urls:
    print(f'Parsing: {category_url}')
    thread = Thread(target = parse_category, args = (category_url,))
    thread.start()
    time.sleep(60)
    #parse_category(category_url)

with open('Links.txt', 'w', encoding = 'UTF-8') as links_file:
    links_file.write('\n'.join(place_links))

print(f'Places found: {len(place_links)}')
'''
