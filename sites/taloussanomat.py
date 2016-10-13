# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	r.encoding = 'ISO-8859-1'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( class_='storyText' )
	for script in text[0].find_all('script'):
		script.decompose()
	for articleData in text[0].find_all(class_ = 'article-data-promo'):
		articleData.decompose()
	text[0].find('div', {'class' : 'readAlso'}).decompose()
	text[0].find('div', {'id' : 'articleMiddleAd'}).decompose()
	text = text[0].get_text(' ', strip = True)
	text = processor.process(text)

	return processor.create_dictionary(url, http_status, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':
	parse("http://www.taloussanomat.fi/politiikka/2015/03/16/kreikka-lyhennamme-velkaamme-sovitusti-imflle/20153273/12", file('taloussanomat.txt', 'w'))
