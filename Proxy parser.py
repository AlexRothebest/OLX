import requests

from bs4 import BeautifulSoup as bs

from threading import Thread

from datetime import datetime

import time


def get_html_proxy(url, proxies = {}):
    return requests.get(url, proxies = proxies, timeout = 1).text


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
