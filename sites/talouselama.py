# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( class_='article-body' )
	for script in text[0].find_all('script'):
		script.decompose()
	for noscript in text[0].find_all('noscript'):
		noscript.decompose()
	text[0].find('div', {'class' : 'share-buttons'}).decompose()
	text[0].find('div', {'class' : 'subscribe-newsletter'}).decompose()
	text = text[0].get_text(' ', strip = True)
	text = processor.process(text)

	return processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':
	parse("http://www.talouselama.fi/vaalit/vaalitebatti/murtuuko+suurten+puolueiden+valta++vaaliraati+vastaa/a2301513", file('talouselama.txt', 'w'))
