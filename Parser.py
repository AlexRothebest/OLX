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


def get_html_proxy(url, proxies = {}):
    return requests.get(url, proxies = proxies, timeout = 7).text


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
    base_url = 'https://awmproxy.net/freeproxy_f9eaf332c06d374.txt'

    proxies_list = [{
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    } for proxy in get_html_proxy(base_url).split('\n')]

    print(f'Proxies found: {len(proxies_list)}\n')

    check_all_proxies(proxies_list)


proxy_file = open('Proxies list.txt', 'w')

good_proxies = []

#thread = Thread(target = search_awmproxy, args = ())
#thread.start()
search_awmproxy()

time.sleep(10)

proxy_file.close()

print(len(good_proxies))

#g = 1 / 0


############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################

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
        thread = Thread(target = get_response, args = ())
        thread.start()
        time.sleep(1)

    return response.text


#parse_place_phone('https://www.olx.ua/obyavlenie/sdam-dvuhkomnatnuyu-obolon-metro-minskaya-IDGomPt.html')
#a = 1 / 0


def parse_place(url, city = 'Харьков'):
    global data_list, links_list

    try:
        html = get_html(url)
        #html = requests.get(url).text

        soup = bs(html, 'html.parser')

        title = soup.find('div', class_ = 'offer-titlebox').h1.text.strip()
        description = soup.find('div', {'id': 'textContent'}).text.strip()
        category = soup.find('td', class_ = 'middle').find_all('li')[-1].a.span.text.strip()
        name = soup.find('div', class_ = 'offer-user__details').h4.a.text.strip()

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
            'phone': '',
            'images': photos,
            'datetime': post_datetime,
            'customs': chars,
            'customs_str': chars_str
        }

        print(title + '\n')
    except:
        if len(links_list) < 100000:
            links_list.append([url, city])


def parse_page(url, city = 'Харьков'):
    global data_list, all_data_urls, unsuccess_urls

    #print(url)

    #html = get_html(url)
    html = requests.get(url).text

    soup = bs(html, 'html.parser')

    urls_list = []
    for a in soup.find_all('a', class_ = 'detailsLink'):
        if 'marginright5' in  a.attrs['class']:
            urls_list.append(a.get('href'))

    if len(urls_list) != 44:
        unsuccess_urls[url] = len(urls_list)

    for url in urls_list:
        if url not in all_data_urls:
            all_data_urls.append(f'{url}-{city}')
            print(f'{url}-{city}')


def parse_category(url, city = 'Харьков'):
    for page_number in range(1, 501):
        page_url = f'{url}?page={page_number}'
        print(url)
        print(page_number)
        thread = Thread(target = parse_page, args = (page_url, city,))
        thread.start()
        time.sleep(0.1)


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


'''
url = 'https://www.olx.ua/obyavlenie/sdam-svoyu-2-h-komn-kv-s-m-studencheskaya-4-min-IDDgNc3.html'
with open('OLX.html', 'w', encoding = 'UTF-8') as file:
    file.write(get_html(url))

d = 1 / 0
'''
'''
with open('Data.json', 'r', encoding = 'UTF-8') as file:
    data = json.loads(file.read())

print(data)

c = 1 / 0
'''

with open('Proxies list.txt', 'r', encoding = 'UTF-8') as file:
    good_proxies = [{
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    } for proxy in file.read().split('\n')]


with open('Proxies list 3.txt', 'r', encoding = 'UTF-8') as file:
    good_proxies_for_selenium = file.read().split('\n')


'''
data_list = {}

url = 'https://www.olx.ua/obyavlenie/prodam-kvartiru-zhk-vorobevy-gory-1-komnatnaya-kvartira-v-rassrochku-IDGodss.html'
with open('OLX.html', 'w', encoding = 'UTF-8') as file:
    file.write(get_html(url))
parse_place(url)
e = 1 / 0
'''

with open('Links OLX.txt', 'r', encoding = 'UTF-8') as file:
    links_list = [[string[:string.rfind('-')], string[string.rfind('-') + 1:]] for string in file.read().split('\n')]

print(len(links_list))


all_data_urls = []
data_list = {}
unsuccess_urls = {}

for link in links_list:
    print(link)
    thread = Thread(target = parse_place, args = (link[0], link[1],))
    thread.start()
    time.sleep(0.1)
    #try:
    #    parse_place(link[0], link[1])
    #except:
    #    print('Error while parsing...')
    #    time.sleep(15)

time.sleep(60)


print('\n\nStarting parsing phones\n\n' + '$' * 1000)

all_links = [link for link in data_list]
#parser = Parser()


print('Starting writing to XML')
write_to_xml(data_list)
print('Writed')

with open('Data.json', 'w', encoding = 'UTF-8') as file:
    file.write(json.dumps(data_list, indent = 4))
    print('*' * 5000)

category_urls = {
    'https://www.olx.ua/nedvizhimost/kha/': 'Харьков',
    'https://www.olx.ua/nedvizhimost/ko/': 'Киев',
    'https://www.olx.ua/nedvizhimost/od/': 'Одесса'
}

'''
page_url = 'https://www.olx.ua/nedvizhimost/kha/'
place_url = 'https://www.olx.ua/obyavlenie/prodam-svoyu-3h-komnatnuyu-kvartiru-IDGpvGh.html'

for category_url in category_urls:
    parse_category(category_url, category_urls[category_url])
#parse_page(page_url)
#parse_place(place_url)
'''

time.sleep(10)

print(data_list)

print(unsuccess_urls)

print(len(all_data_urls))

with open('Links.txt', 'w', encoding = 'UTF-8') as file:
    file.write('\n'.join(all_data_urls))
