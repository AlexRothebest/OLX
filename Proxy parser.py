from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

import requests
from requests.exceptions import ConnectionError, ProxyError

from bs4 import BeautifulSoup as bs

from threading import Thread

from datetime import datetime

import time


def get_html(url, proxies = {}):
    return requests.get(url, proxies = proxies, timeout = 1).text


def check_proxy(proxy):
    global good_proxies

    proxies = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}',
        #'ftp': f'ftp://{proxy}',
        #'ssl': f'ssl://{proxy}'
    }

    start_time = datetime.now()
    try:
        #session = requests.Session()
        #session.proxies = proxies
        response = requests.get('https://icanhazip.com', proxies = proxies, timeout = 3)
        print(response.text)
        print(proxy, (datetime.now() - start_time).seconds)
        if (datetime.now() - start_time).seconds < 3:
            good_proxies.append(proxies)
            return True
        else:
            return False
    except:
        return False


#print(check_proxy('103.251.57.23:60083'))
#a = 1 / 0


def check_all_proxy():
    global proxy_list

    lol = {
        True: 'good',
        False: 'bad'
    }
    print('\nStarting checking proxies')
    for proxy in proxy_list:
        thread = Thread(target = check_proxy, args = (proxy,))
        thread.start()
        time.sleep(0.1)
        #print(proxy + ' --- ' + lol[check_proxy(proxy)])

    time.sleep(11)
    print('Finish')


def check_proxy2(proxies, proxy):
    global good_proxies, file

    start_time = datetime.now()
    try:
        html = get_html('https://icanhazip.com', proxies).strip()
        print(f'HTML: {html} {proxy} {(datetime.now() - start_time).seconds}\n\n')
        if 0 < len(html) < 25:   #and (datetime.now() - start_time).seconds <= 2:
            good_proxies.append(proxies)
            file.write(f'{proxy} {(datetime.now() - start_time).seconds}\n')
            #file.save()
            file.close()
            file = open('Proxies list.txt', 'a')
    except ConnectionError:
        pass
    except ProxyError:
        pass
    except Exception as e:
        raise e
        #pass


def check_all_proxies2(proxies_list):
    for proxies in proxies_list:
        proxy = proxies['https'][8:]
        print(proxy)
        thread = Thread(target = check_proxy2, args = (proxies, proxy,))
        thread.start()
        time.sleep(0.1)
        #check_proxy2(proxies)


def search_awmproxy():
    base_url = 'https://awmproxy.net/freeproxy_eca7bb3bbb457e2.txt'

    proxies_list = [{
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    } for proxy in get_html(base_url).split('\n')]

    print(f'Proxies found: {len(proxies_list)}\n')

    check_all_proxies2(proxies_list)


def search_free_proxy_list():
    global proxy_list

    #base_url = 'https://free-proxy-list.net'
    base_url = 'https://www.sslproxies.org'

    options = Options()
    options.add_argument('--headless')

    driver = Chrome('chromedriver.exe', options = options)
    driver.get(base_url)

    for i in range(15):
        time.sleep(0.5)

        for tr in driver.find_element_by_id('proxylisttable').find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr'):
            proxy = f"{tr.find_elements_by_tag_name('td')[0].text}:{tr.find_elements_by_tag_name('td')[1].text}"
            if proxy not in proxy_list:
                proxy_list.append(proxy)
                print(proxy)

        driver.execute_script("arguments[0].click()", driver.find_element_by_id('proxylisttable_next'))

    driver.quit()


def search_proxy_sale():
    global proxy_list

    image_list = {
        'https://free.proxy-sale.com/wp-content/uploads/fps/port_images/59f3846408407d3143db9f405531ec65.png': 8888,
        'https://free.proxy-sale.com/wp-content/uploads/fps/port_images/299db15b3a5f119636dba89962650a03.png': 8123,
        'https://free.proxy-sale.com/wp-content/uploads/fps/port_images/89b09fc0f66997e8421d8061030c983a.png': 8080,
        'https://free.proxy-sale.com/wp-content/uploads/fps/port_images/e3f65f8ff04504869f3e163d532381f2.png': 3128,
        'https://free.proxy-sale.com/wp-content/uploads/fps/port_images/b8c08b828f5c8138a86e18667aa60824.png': 808,
        'https://free.proxy-sale.com/wp-content/uploads/fps/port_images/4941ccdc296f1e8d57e6c618bfdc2b76.png': 4444,
        'https://free.proxy-sale.com/wp-content/uploads/fps/port_images/e58a3cb12d4b567523fec022a24c254a.png': 1080,
        'https://free.proxy-sale.com/wp-content/uploads/fps/port_images/3a368e4edca060c47c2a5bc0aa6ff0dc.png': 5220,
        'https://free.proxy-sale.com/wp-content/uploads/fps/port_images/a089dd618ecb532de560880729150af9.png': 8118,
        'https://free.proxy-sale.com/wp-content/uploads/fps/port_images/a1d3cebf33ed2852e5410946c9beb04b.png': 4145
    }

    options = Options()
    options.add_argument('--headless')

    driver = Chrome('chromedriver.exe', options = options)
    for page in range(1, 2):
        driver.get(f'https://free.proxy-sale.com/?proxy_page={page}')

        finded = False
        time_start = datetime.now()
        while not finded and (datetime.now() - time_start).seconds < 10:
            for tr in driver.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr'):
                proxy = ''
                try:
                    proxy = f"{tr.find_element_by_tag_name('td').text}:{image_list[tr.find_element_by_tag_name('img').get_attribute('src')]}"
                except KeyError:
                    if tr.find_elements_by_tag_name('td')[1].text.strip() != '':
                        proxy = f"{tr.find_element_by_tag_name('td').text}:{tr.find_elements_by_tag_name('td')[1].text}"
                    else:
                        print(tr.find_element_by_tag_name('img').get_attribute('src'))
                if proxy not in proxy_list and proxy != '':
                    proxy_list.append(proxy)
                    print(proxy)

                finded = True

            time.sleep(1)

    driver.quit()


def search_proxy_list():
    global proxy_list

    options = Options()
    options.add_argument('--headless')

    driver = Chrome('chromedriver.exe', options = options)

    for page_num in range(1,11):
        driver.get(f'http://proxy-list.org/russian/index.php?p={page_num}')
        time.sleep(1)
        for li in driver.find_elements_by_class_name('proxy')[1:]:
            proxy = li.text
            if proxy not in proxy_list:
                proxy_list.append(proxy)
                print(proxy)

    driver.quit()


file = open('Proxies list.txt', 'w')

proxy_list = []
good_proxies = []

search_awmproxy()
#search_free_proxy_list()
#search_proxy_sale()
#search_proxy_list()

#check_all_proxy()

file.close()

print(f'Proxies found: {len(good_proxies)}\n\nStarting parsing')

'''
proxy_list = [
    '188.225.27.151:3128',
    '52.74.155.41:8080',
    '138.117.113.221:8080',
    '36.77.168.11:8888',
    '116.58.247.156:8080',
    '49.48.42.175:8080',
    '103.206.100.189:8080',
    '1.20.227.241:8080',
    '157.245.68.27:1080',
    '109.111.134.200:8080',
    '36.90.101.62:8080',
    '101.108.13.209:8080',
    '210.22.5.117:3128',
    '163.172.152.52:8811',
    '51.158.111.229:8811',
    '61.7.191.45:8080',
    '36.77.168.11:8888',
    '14.207.11.21:8080',
    '170.254.221.184:8080',
    '110.77.231.145:80',
    '58.153.112.168:8080',
    '78.40.226.61:3128'
]
'''
#proxy_list = ['194.213.43.166:38170', '103.106.238.230', '167.249.171.42', '171.7.58.128', '5.15.55.98', '81.163.58.15', '131.196.141.221', '95.154.104.147', '178.63.119.219', '195.62.70.254', '82.135.148.201', '195.182.152.238', '27.68.135.14', '160.19.245.61', '163.53.199.2', '181.115.46.114', '103.119.244.10', '176.241.89.36', '186.227.213.234', '94.158.165.19', '185.162.142.81', '138.121.155.127', '103.250.166.17', '113.53.82.92', '91.214.60.141', '62.122.18.7', '103.21.92.18', '180.253.122.118', '91.219.166.51', '195.138.92.152', '103.250.153.242', '46.255.98.14', '31.40.136.30', '118.172.211.37', '176.121.48.48', '92.52.186.123']
good_proxies = [{
    'http': f'http://{proxy}',
    'https': f'https://{proxy}'
} for proxy in proxy_list]

for proxies in good_proxies:
    print(proxies['http'][7:])
    try:
        html = get_html('https://icanhazip.com', proxies)
        print(html)
        #my_ip = bs(html, 'html.parser').find('p', {'id': 'shownIpv4'}).text.strip()
        #print(my_ip)
        print('\n\n')
    except:
        pass

# 188.225.27.151:3128
# 52.74.155.41:8080
# 138.117.113.221:8080
# 36.77.168.11:8888
# 116.58.247.156:8080
# 49.48.42.175:8080
# 103.206.100.189:8080
# 1.20.227.241:8080
# 157.245.68.27:1080
# 109.111.134.200:8080
# 36.90.101.62:8080
# 101.108.13.209:8080
# 210.22.5.117:3128
# 163.172.152.52:8811
# 51.158.111.229:8811
# 61.7.191.45:8080
# 36.77.168.11:8888
# 14.207.11.21:8080
# 170.254.221.184:8080
# 110.77.231.145:80
# 58.153.112.168:8080
# 78.40.226.61:3128
