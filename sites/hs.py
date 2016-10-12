# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )

	http_status = r.status_code
	if r.status_code == 404:
		return

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( id = 'main-content' )

	categories = [str( article.find( class_ = 'article-category' ).get_text().strip().encode('utf8') )]

	datetime_data = article.find_all( 'time' )
	for datetime_string in datetime_data:
		datetime_string = datetime_string.get_text( strip = True ).replace( 'Päivitetty:'.decode('utf8'), '' )


	text = soup.find_all( class_ = "article-text-content" )
	for div in text[0].find_all( 'div'):
		div.decompose()
	text = text[0].get_text(' ', strip=True)
	text = processor.process(text)

	return processor.create_dictionary(url, http_status, categories, [''], '', '', '', text, [''], [''])

if __name__ == '__main__':

	parse("http://www.hs.fi/paakirjoitukset/a1428030701507", file('hs.txt', 'w'))
