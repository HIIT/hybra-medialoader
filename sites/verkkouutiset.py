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

	ingress = soup.find_all( class_ = 'ingress')
	text = soup.find_all( class_='articlepart-1' )
	for slides in text[0].find_all( class_ ='flexslider'):
		slides.decompose()
	content = ingress[0].get_text(' ', strip = True)
	content += ' ' + text[0].get_text(' ', strip = True)
	text = processor.process(content)

	return processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':
	parse("http://www.verkkouutiset.fi/talous/ammattisijoittajan_neuvot-33352", file('verkkouutiset.txt', 'w'))
