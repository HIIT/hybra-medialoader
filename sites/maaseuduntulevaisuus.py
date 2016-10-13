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

	text = soup.find_all( class_='article-single-section__content' )
	text = text[0].get_text(' ', strip = True)
	text = processor.process(text)

	return processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':
	parse("http://www.maaseuduntulevaisuus.fi/maatalous/nurmipelloille-voi-tulla-k%C3%A4ytt%C3%B6rajoituksia-1.76216", file('maaseudun.txt', 'w'))
