import requests

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains

from threading import Thread

from bs4 import BeautifulSoup as bs

from random import randint

from datetime import datetime

import time

import xml.etree.ElementTree as xml
import xml.dom.minidom as minidom

import json

import os

import shutil

import copy

from importlib import import_module


try:
    pass
    import_module('Proxy parser.py')
except:
    pass

try:
    pass
    import_module('Category parser.py')
except:
    pass


def get_html(url):
    global good_proxies, something_happends

    something_happends = True

    while True:
        try:
            something_happends = True

            proxies = good_proxies[randint(0, len(good_proxies) - 1)]

            response_local = requests.get(url, proxies = proxies, timeout = 7)
            if response_local.status_code == 200:
                response = response_local
                break
        except:
            #pass
            print(f'Error...( {url}')

    something_happends = False

    return response.text


def parse_seller(url):
    global all_sellers

    html = get_html(url)
    soup = bs(html, 'html.parser')

    phone = soup.find('div', {'data-icon': 'phone'}).text.strip().replace('\n', ', ')
    city = soup.find('address', {'data-icon': 'location-filled'}).find_all('span')[-1].text.strip()

    try:
        number_of_pages = int(soup.find('div', class_ = 'pager').find_all('span', class_ = 'item')[-1].a.text.strip())
    except:
        number_of_pages = 1

    # number_of_pages = 1

    seller_links = [h3.a.get('href') for h3 in soup.find_all('h3', class_ = 'x-large')]
    print(f'Phone: {phone}\nPages: {number_of_pages}')
    for page_number in range(2, number_of_pages + 1):
        page_url = f'{url}/shop/?page={page_number}'

        html = get_html(page_url)
        soup = bs(html, 'html.parser')

        for h3 in soup.find_all('h3', class_ = 'x-large'):
            seller_links.append(h3.a.get('href'))

    print(f'Phone: {phone}\nPages: {number_of_pages}\nLinks: {seller_links}')

    all_sellers[url] = [phone, city, seller_links]

    return phone


def download_images(name, urls):
    name = name.replace('\ '[0], ' ').replace('/', ' ').replace('?', ' ').replace(':', ' ').replace('|', ' ').replace('!', ' ')\
               .replace('<', ' ').replace('>', ' ').replace('"', ' ').replace('*', ' ').replace(".", ' ').strip()
    try:
        os.mkdir(f'photos/{name}')
    except:
        pass

    for image_num, url in enumerate(urls):
        image_response = requests.get(url, stream = True)
        with open(f'photos/{name}/image{image_num + 1}.png', 'wb') as image_file:
            shutil.copyfileobj(image_response.raw, image_file)


def parse_place(url, city, parse_without_checking_category, phone = ''):
    global data_list, links_list, all_sellers, flags, all_categories

    if '#' in url:
        url = url[:url.find('#')]

    flags[url] = False

    name_of_photo_folder = url[url.rfind('/') + 1 : url.rfind('.html')]

    try:
        html = get_html(url)
        while len(html) < 10000:
            html = get_html(url)
        soup = bs(html, 'html.parser')

        title = soup.find('div', class_ = 'offer-titlebox').h1.text.strip()
        print(f'HTML received for {title}' + '&' * 200)
        description = soup.find('div', {'id': 'textContent'}).text.strip()
        category = soup.find('td', class_ = 'middle').find_all('li')[-1].a.span.text.strip()
        if parse_without_checking_category:
            if category not in all_categories:
                all_categories.append(category)
        else:
            if category not in all_categories:
                q = 1 / 0
        name = soup.find('div', class_ = 'offer-user__details').h4.a.text.strip()

        if phone == '':
            seller_link = soup.find('div', class_ = 'offer-user__details').h4.a.get('href')
            try:
                phone = all_sellers[seller_link]
            except:
                #print(f'Name: {name}\nSeller link: {seller_link}')
                if seller_link[-7:] == '.olx.ua':
                    print('Good seller was found')
                    phone = parse_seller(seller_link)
                    #all_sellers.append(seller_link)
                else:
                    print('NO phone number(((\n\n')
                    flags[url] = True
                    return

        price = soup.find('div', class_ = 'price-label').strong.text.strip()
        if price.find('грн') != -1:
            currency = 'грн'
        elif price.find('$') != -1:
            currency = '$'
        elif price.find('руб') != -1:
            currency = 'руб'
        price = price[:price.find(currency)].strip()

        photos = [img.get('src') for img in soup.find_all('img', class_ = 'bigImage')]

        post_datetime = soup.find('div', class_ = 'offer-titlebox__details').em.text.strip()
        post_datetime = post_datetime[post_datetime.find('   ') + 3 : post_datetime.find('Номер')].strip()
        if post_datetime[0] == 'в':
            post_datetime = post_datetime[1:].strip()[:-1]

        chars = {}
        for td in soup.find('table', class_ = 'details').find_all('td', class_ = 'col'):
            prop = td.table.tr.th.text.strip()
            value_list = td.table.tr.td.strong.find_all('a')
            if len(value_list) == 0:
                chars[prop] = td.table.tr.td.text.replace('м²', '').replace('сот.', '').replace('м²', 'га').strip()
            else:
                chars[prop] = ', '.join(a.text.replace('м²', '').replace('сот.', '').replace('м²', 'га').strip() for a in value_list)

        chars_str = ''
        for prop in chars:
            chars_str += f'{prop}:{chars[prop]};'

        download_images(name_of_photo_folder, photos)

        photos = [f'photos/{name_of_photo_folder}/image{image_number}.jpg' for image_number in range(1, len(photos) + 1)]

        data_list[url] = {
            'title': title,
            'description': description,
            'category': category,
            'name': name,
            'price': price,
            'currency': currency,
            'city': city,
            'countryid': 'UKR',
            'country': 'Ukraine',
            'phone': phone,
            'images': photos,
            'datetime': post_datetime,
            'customs': chars,
            'customs_str': chars_str
        }

        print(title + '\n\n')
    except Exception as e:
        flags[url] = True

        print('Error on parsing\n\n')

        with open('Error HTML.html', 'w', encoding = 'UTF-8') as file:
            file.write(html)

        raise e

        if len(links_list) < 100000:
            links_list.append([url, city])

    flags[url] = True


def write_to_xml(data):
    yml = xml.Element('yml')

    def write_place_to_yml(place):
        nonlocal yml

        listing = xml.Element('listing')
        yml.append(listing)

        title = xml.SubElement(listing, 'title', lang = 'ru_RU')
        title.text = f"<![CDATA[{place['title']}]]>"

        content = xml.SubElement(listing, 'content', lang = 'ru_RU')
        content.text = f"<![CDATA[{place['description']}]]>"

        category = xml.SubElement(listing, 'category', lang = 'ru_RU')
        category.text = place['category']

        contactname = xml.SubElement(listing, 'contactname')
        contactname.text = place['name']

        price = xml.SubElement(listing, 'price')
        price.text = place['price']

        currency = xml.SubElement(listing, 'currency')
        currency.text = place['currency']

        city = xml.SubElement(listing, 'city')
        city.text = place['city']

        region = xml.SubElement(listing, 'region')
        region.text = place['city']

        countryid = xml.SubElement(listing, 'countryid')
        countryid.text = place['countryid']

        country = xml.SubElement(listing, 'country')
        country.text = place['country']

        telfon = xml.SubElement(listing, 'telfon')
        telfon.text = place['phone']

        for photo in place['images']:
            image = xml.SubElement(listing, 'image')
            image.text = photo

        for prop in place['customs']:
            char = xml.SubElement(listing, 'custom', name = prop)
            char.text = place['customs'][prop]

        datetime = xml.SubElement(listing, 'datetime')
        datetime.text = place['datetime']

    new_data = data.copy()
    for url in new_data:
        for iterations in range(10):
            print('dfklgmklfmkfmklfkmgsghmsfmlgkfmhlmhgfm')
            
            place = new_data[url]

            print(url)

            old_yml = copy.copy(yml)

            try:
                write_place_to_yml(place)
                data = xml.tostring(yml, encoding='unicode', method='xml')
                break
            except Exception as e:
                # raise e

                yml = old_yml

    print(f'YML type: {type(yml)}')

    with open('XML Data.xml', 'w', encoding = 'UTF-8') as file:
        data = minidom.parseString(str(xml.tostring(yml))[2 : -1]).toprettyxml()[: -1].replace('&lt;', '<').replace('&gt;', '>').replace('&quot', '"')
        print(data)
        # print(minidom.parseString(str(xml.tostring(yml))[2 : -1]).toprettyxml()[: -1].replace('&lt;', '<').replace('&gt;', '>').replace('&quot', '"'))
        if len(data) > 1000:
            file.write(minidom.parseString(str(xml.tostring(yml))[2 : -1]).toprettyxml()[: -1].replace('&lt;', '<').replace('&gt;', '>').replace('&quot', '"'))


try:
    shutil.rmtree('photos')
except:
    pass
time.sleep(1)
os.mkdir('photos')


with open('Perfect proxy list.txt', 'r', encoding = 'UTF-8') as file:
    good_proxies = [{
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    } for proxy in file.read().split('\n')]


with open('Links.txt', 'r', encoding = 'UTF-8') as file:
    links_list = [[string[:string.rfind('-')], string[string.rfind('-') + 1:]] for string in file.read().split('\n')]

# links_list = links_list[:20]

print(f'Links to parse: {len(links_list)}')

all_data_urls = []
all_sellers = {}
data_list = {}
unsuccess_urls = {}
something_happends = False
flags = {}
all_categories = []

write_to_xml(data_list)

# w = 1 / 0

# parse_place('https://www.olx.ua/obyavlenie/1komn-zhk-mira-1-m-maselskogo-r-n-novye-doma-htz-36m2-remont-IDGp5YY.html', 'Kharkov', True)
# a = 1 / 0

for link in links_list:
    print(link)
    thread = Thread(target = parse_place, args = (link[0], link[1], True,))
    thread.start()
    time.sleep(0.1)

time.sleep(60)

start_time = datetime.now()
while False in [flags[key] for key in flags] and (datetime.now() - start_time).seconds < 1000:
    print('Flags are not ready')
    for key in flags:
        if not flags[key]:
            print(key)
    print((datetime.now() - start_time).seconds)
    print('\n')
    time.sleep(10)


all_place_urls = [url for url in data_list]
flags = {}

new_all_sellers = all_sellers.copy()
for seller_url in new_all_sellers:
    for url in new_all_sellers[seller_url][2]:
        if url not in all_place_urls:
            print(f'Seller URL: {url}')
            thread = Thread(target = parse_place,
                            args = (url, new_all_sellers[seller_url][1], False, new_all_sellers[seller_url][0],))
            thread.start()
            time.sleep(0.1)

time.sleep(60)

start_time = datetime.now()
while False in [flags[key] for key in flags] and (datetime.now() - start_time).seconds < 1000:
    print('Flags are not ready (2)')
    time.sleep(10)

print('Starting writing to XML')
write_to_xml(data_list)
print('Writed')

with open('Data.json', 'w', encoding = 'UTF-8') as file:
    file.write(json.dumps(data_list, indent = 4))
    print('*' * 5000)

print(data_list)

print(unsuccess_urls)

print(len(all_data_urls))

# with open('Links.txt', 'w', encoding = 'UTF-8') as file:
#     file.write('\n'.join(all_data_urls))