import requests

from bs4 import BeautifulSoup as bs

from random import randint

import time

import re


with open('Links OLX.txt', 'r') as file:
	links_list = file.read().split('\n')

link = links_list[randint(0, len(links_list) - 1)]
url = link[:link.rfind('#')]
print(f'Target URL: {url}')

#b = 1 / 0


with open('Perfect proxy list.txt', 'r') as file:
	proxy_list = file.read().split('\n')

proxy = proxy_list[randint(0, len(proxy_list) - 1)]
proxies = {
	'http': f'http://{proxy}',
	'https': f'https://{proxy}',
	'ssl': f'ssl://{proxy}'
}

print(f'Proxy server used: {proxy}\n')


session = requests.Session()
session.proxies = proxies

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36'
}
#url = 'https://www.olx.ua/obyavlenie/prodam-dachu-igren-2-etazha-3-komnaty-5-sotok-uchastok-IDFlvNA.html'
print('Request was sent')
while True:
	try:
		response = session.get(url, timeout = 7)
		break
	except:
		print('Timeout error, setting new proxies')

		proxy = proxy_list[randint(0, len(proxy_list) - 1)]
		proxies = {
			'http': f'http://{proxy}',
			'https': f'https://{proxy}',
			'ssl': f'ssl://{proxy}'
		}
		session.proxies = proxies

		print(f'\nNew proxy server: {proxy}\nSending new request')
		time.sleep(1)
print('Response was received successfully\n')
soup = bs(response.content.decode('UTF-8'), 'html.parser')


'''
with open('response.html', 'w') as response_file:
	response_file.write(response.content.decode('UTF-8'))

with open('cookies.txt', 'w') as cookies_file:
	cookies_file.write(str(response.cookies))
'''

raw_text = [elem for elem in soup.find_all('script') if 'phoneToken' in elem.text][0].text.strip()
token = re.findall(r"['\"](.*?)['\"]", raw_text)[0]
seller_id = url.split('ID')[1].split('.')[0]
phone_url = f'https://www.olx.ua/ajax/misc/contact/phone/{seller_id}/?pt={token}'

print(f'URL to get phone number: {phone_url}')

time.sleep(3)

#a = 1 / 0
'''
headers = {
	'authority': 'www.olx.ua',
	'method': 'GET',
	'path': f'/ajax/misc/contact/phone/{seller_id}/?pt={token}',
	'scheme': 'https',
	'accept': '*/*',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
    'referer': url,
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
'''
print('\nSending AJAX reques to get phone number')
headers = {
	'path': f'/ajax/misc/contact/phone/{seller_id}/?pt={token}',
    'referer': url,
    'X-Requested-With': 'XMLHttpRequest'
}
while True:
	try:
		response = session.get(phone_url, headers = headers)
		break
	except:
		print('Timeout error, setting new proxies')

		proxy = proxy_list[randint(0, len(proxy_list) - 1)]
		proxies = {
			'http': f'http://{proxy}',
			'https': f'https://{proxy}',
			'ssl': f'ssl://{proxy}'
		}
		session.proxies = proxies

		print(f'\nNew proxy server: {proxy}\nSending new request')
		time.sleep(1)

'''
proxy = proxy_list[randint(0, len(proxy_list) - 1)]
proxies = {
	'http': f'http://{proxy}',
	'https': f'https://{proxy}',
	'ssl': f'ssl://{proxy}'
}
response = requests.get(phone_url, proxies = proxies, headers = headers)   #, cookies = response.cookies)
'''

print(f'\nResponse length: {len(response.content)}')
#print(f'Response: {response.content}')
print(f'Response: {response.json()}')