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
    city VARCHAR(255), countryId VARCHAR(255), country VARCHAR(255), address VARCHAR(255), phone VARCHAR(255),\
    images VARCHAR(255), datetime VARCHAR(255), customs TEXT)')
    cols = ['title', 'description ', 'category', 'name', 'price', 'currency',\
            'city', 'countryId', 'country', 'address', 'phone', 'images', 'datetime', 'customs']

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

    proxies = good_proxies[randint(0, len(good_proxies) - 1)]

    return requests.get(url, proxies = proxies).text


def get_html_proxy(url, proxies = {}):
    return requests.get(url, proxies = proxies, timeout = 1).text


def parse_place(driver, url):
    #url = 'http://besplatka.ua/obyavlenie/arenda-doma-shale-kottedzha-f3d173'
    ip_url = 'http://icanhazip.com'

    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = '51.158.68.133:8811'
    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    options = Options()
    options.add_argument('--headless')

    driver = Chrome('chromedriver.exe', options = options, desired_capabilities = capabilities)

    driver.get(url)
    #driver.get(ip_url)

    #time.sleep(5)

    print(driver.page_source)

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
    city = driver.find_element_by_xpath("//span[@itemprop = 'addressLocality']").text.strip()
    photos = [img.get_attribute('src') for img in driver.execute_script("return document.getElementsByClassName('message-image ms-slider-container count-9')[0].getElementsByTagName('img')")]
    datetime = driver.execute_script("return document.getElementsByClassName('list-inline card-info hidden-xs')[0].children[1].innerText.trim()")
    if datetime.find(',') != -1:
        datetime = datetime[:datetime.find(',')]
    datetime = datetime[datetime.rfind(' ') + 1:]
    chars = {
        prop_block.find_element_by_class_name('key').get_attribute('innerText').strip():\
        prop_block.find_element_by_class_name('value').get_attribute('innerText').strip()\
        for prop_block in driver.find_elements_by_class_name('property')
    }
    print(name)
    print(chars)


def check_proxy(proxies, proxy):
    global good_proxies, file

    start_time = datetime.now()
    try:
        html = get_html_proxy('https://icanhazip.com', proxies).strip()
        print(f'HTML: {html} {proxy} {(datetime.now() - start_time).seconds}\n\n')
        if 0 < len(html) < 25:
            good_proxies.append(proxies)
            file.write(f'{proxy} {(datetime.now() - start_time).seconds}\n')
            file.close()
            file = open('Proxies list.txt', 'a')
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
    base_url = 'https://awmproxy.net/freeproxy_eca7bb3bbb457e2.txt'

    proxies_list = [{
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    } for proxy in get_html_proxy(base_url).split('\n')]

    print(f'Proxies found: {len(proxies_list)}\n')

    check_all_proxies(proxies_list)


file = open('Proxies list.txt', 'w')

good_proxies = []

search_awmproxy()

file.close()

for page_number in range(500):
    url = f'https://besplatka.ua/kiev/nedvizhimost/page/{page_number}'
    html = get_html(url)
    soup = bs(html, 'html.parser')
    links = ['https://besplatka.ua' + a.get('href') for a in soup.find_all('a', class_ = 'm-title')]
    print('\n'.join(links))
