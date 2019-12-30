from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.proxy import Proxy, ProxyType


prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
#prox.http_proxy = '51.158.68.133:8811'
#prox.http_proxy = '167.172.247.68:8080'
#prox.http_proxy = '167.172.35.224:8080'
prox.http_proxy = '163.172.128.177:8811'
#prox.http_proxy = '51.158.99.51:8811'
#prox.http_proxy = ''
#prox.http_proxy = ''
#prox.http_proxy = ''
#prox.http_proxy = ''
#prox.http_proxy = ''
#prox.http_proxy = ''
#prox.http_proxy = ''
#prox.http_proxy = ''
#prox.http_proxy = ''
#prox.http_proxy = ''
#prox.http_proxy = ''

capabilities = webdriver.DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)

driver = Chrome('chromedriver.exe', desired_capabilities = capabilities)

driver.get('http://icanhazip.com')
