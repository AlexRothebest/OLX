# Ссылка на список прокси, он действителен только одни сутки, поэтому надо его регулярно обновлять
# (обновлять надо только в начале работы программы). Я беру его отсюда https://awmproxy.net/freeproxy.php
# Если найдёте другой список прокси, в котором их. желательно, было бы побольше, будет отлично)
proxy_list_link = 'https://awmproxy.net/freeproxy_cc81c67dc38e89d.txt'


# Список ссылок на категории, которые надо парсить
# Формат: "ссылка": ["название_города", количество_страниц_которое_нужно_парсить]
category_urls = {
	'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/kvartira/kha/?search%5Bfilter_float_price%3Afrom%5D=10000&search%5Bfilter_float_price%3Ato%5D=18000&currency=USD': ['Харьков', 10],
	# 'https://www.olx.ua/nedvizhimost/ko/': ['Киев', 161]
}