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


class Parser():
    def reload(self):
        global good_proxies_for_selenium

        try:
            self.driver.quit()
        except:
            pass

        proxy = good_proxies_for_selenium[randint(0, len(good_proxies_for_selenium) - 1)]

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
        options.add_argument('--headless')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')

        self.driver = Chrome('chromedriver.exe', options = options, desired_capabilities = capabilities)

    def __init__(self):
        global all_links

        self.reload()

        while len(all_links) > 0:
            link = all_links.pop(0)

            try:
                self.parse_place_phone(link)
            except:
                self.reload()
                #pass

            #self.reload()
            time.sleep(5)

    def parse_place_phone(self, url):
        global data_list

        def driver_get(driver, url):
            driver.get(url)

        driver = self.driver

        #driver.get('https://icanhazip.com')
        #print(driver.page_source)

        #thread = Thread(target = driver_get, args = (driver, url,))
        #thread.start()
        driver.get(url)

        #with open('OLX 3.html', 'w', encoding = 'UTF-8') as file:
        #    file.write(driver.page_source)

        #time.sleep(1)

        #hover = ActionChains(driver).move_to_element(driver.execute_script('''return document.querySelector("div[data-rel='phone'] strong")'''))
        #hover.perform()

        #time.sleep(1)

        start_time = datetime.now()
        clicked = False
        while (datetime.now() - start_time).seconds < 10:
            try:
                driver.execute_script('''document.querySelector("div[data-rel='phone'] strong").click()''')
                clicked = True
                break
            except:
                time.sleep(0.1)
                print('ofiojiojjgtrjtjgriitorjgr')

        if not(clicked):
            f = 1 / 0

        time.sleep(1)

        start_time = datetime.now()
        while (datetime.now() - start_time).seconds < 10:
            try:
                phone = driver.find_element_by_xpath("//div[@data-rel='phone']/strong").text.strip().replace(' ', '').replace('-', '')
                if phone.find('x') != -1:
                    b = 1 / 0
                break
            except:
                time.sleep(3)
                #print('iorjgih')

        print(phone)

        data_list[url]['phone'] = phone

        time.sleep(1)


#parse_place_phone('https://www.olx.ua/obyavlenie/sdam-dvuhkomnatnuyu-obolon-metro-minskaya-IDGomPt.html')
#a = 1 / 0


############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################

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

    #number_of_pages = 1

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


def parse_place(url, city, phone = ''):
    global data_list, links_list, all_sellers

    try:
        html = get_html(url)
        while len(html) < 10000:
            html = get_html(url)
        soup = bs(html, 'html.parser')

        title = soup.find('div', class_ = 'offer-titlebox').h1.text.strip()
        print(f'HTML received for {title}' + '&' * 200)
        description = soup.find('div', {'id': 'textContent'}).text.strip()
        category = soup.find('td', class_ = 'middle').find_all('li')[-1].a.span.text.strip()
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
                chars[prop] = td.table.tr.td.text.strip()
            else:
                chars[prop] = ', '.join(a.text.strip() for a in value_list)

        chars_str = ''
        for prop in chars:
            chars_str += f'{prop}:{chars[prop]};'

        download_images(title, photos)

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
        print('Error on parsing\n\n')

        with open('Error HTML.html', 'w', encoding = 'UTF-8') as file:
            file.write(html)

        raise e

        if len(links_list) < 100000:
            links_list.append([url, city])


def write_to_xml(data):
    yml = xml.Element('yml')

    for url in data:
        print('dfklgmklfmkfmklfkmgsghmsfmlgkfmhlmhgfm')
        place = data[url]

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

    with open('XML Data.xml', 'w', encoding = 'UTF-8') as file:
        print(minidom.parseString(str(xml.tostring(yml))[2 : -1]).toprettyxml()[: -1].replace('&lt;', '<').replace('&gt;', '>'))
        file.write(minidom.parseString(str(xml.tostring(yml))[2 : -1]).toprettyxml()[: -1].replace('&lt;', '<').replace('&gt;', '>').replace('&quot', '"'))


try:
    shutil.rmtree('photos')
except:
    pass
time.sleep(1)
os.mkdir('photos')


with open('Proxy list.txt', 'r', encoding = 'UTF-8') as file:
    good_proxies = [{
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    } for proxy in file.read().split('\n')]


with open('Links 2.txt', 'r', encoding = 'UTF-8') as file:
    links_list = [[string[:string.rfind('-')], string[string.rfind('-') + 1:]] for string in file.read().split('\n')]

'''
with open('Links OLX.txt', 'r', encoding = 'UTF-8') as file:
    links_list = [[string[:string.rfind('-')], string[string.rfind('-') + 1:]] for string in file.read().split('\n')]

with open('Links.txt', 'r', encoding = 'UTF-8') as file:
    links_list2 = [[string[:string.rfind('-')], string[string.rfind('-') + 1:]] for string in file.read().split('\n')]

for link_number, link in enumerate(links_list2):
    if link not in links_list:
        links_list.append(link)
        print(f'{link}\n{len(links_list)}/{len(links_list) + link_number}')

with open('Links 2.txt', 'w', encoding = 'UTF-8') as file:
    file.write('\n'.join('-'.join(link) for link in links_list))
'''

print(f'Links to parse: {len(links_list)}')

#e = 1 / 0

all_data_urls = []
all_sellers = {}
data_list = {}
unsuccess_urls = {}
something_happends = False

for link in links_list[:10]:
    print(link)
    thread = Thread(target = parse_place, args = (link[0], link[1],))
    thread.start()
    #parse_place(link[0], link[1])
    time.sleep(0.1)

time.sleep(120)

while something_happends:
    time.sleep(30)

all_place_urls = [url for url in data_list]

for seller_url in all_sellers:
    for url in all_sellers[seller_url][2]:
        if url not in all_place_urls:
            print(f'Seller URL: {url}')
            thread = Thread(target = parse_place,
                            args = (url, all_sellers[seller_url][1], all_sellers[seller_url][0]))
            thread.start()
            time.sleep(0.1)
            #parse_place(url, all_sellers[seller_url][1], all_sellers[seller_url][0])
            #break

time.sleep(120)

while something_happends:
    time.sleep(30)

print('Starting writing to XML')
write_to_xml(data_list)
print('Writed')

with open('Data.json', 'w', encoding = 'UTF-8') as file:
    file.write(json.dumps(data_list, indent = 4))
    print('*' * 5000)

print(data_list)

print(unsuccess_urls)

print(len(all_data_urls))

#with open('Links.txt', 'w', encoding = 'UTF-8') as file:
#    file.write('\n'.join(all_data_urls))