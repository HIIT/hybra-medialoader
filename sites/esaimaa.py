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

	menu = soup.find( id = 'menu2' )
	category = menu.find( class_ = 'selected' ).get_text(strip = True)
	categories = [str( category.encode('utf8') )]

	article = soup.find( class_ = 'news-item')
	for script in article.find_all( 'script' ):
		script.decompose()

	author = soup.find_all( class_ = 'lahde' )
	author = author[0].get_text(' ', strip = True) + ' ' + author[1].get_text(' ', strip = True)

	datetime_data = article.find( class_ = 'date').get_text(' ', strip = True)
	datetime_list = [datetime.strptime( datetime_data, "%d.%m.%Y %H:%M" )]

	title = article.find('h1').get_text(strip = True)

	text = article.find_all( id='main_text' )
	for div in text[0].find_all( 'div', {'class' : 'lahde'} ):
		div.decompose()
	text = text[0].get_text(' ', strip=True)
	text = processor.process(text)

	images = article.find_all( 'img' )
	image_src = [None]
	for img in images:
		image_src.append( str( "http://www.esaimaa.fi" + img['src'].encode('utf8') ) )
	image_src.pop(0)

	return processor.create_dictionary(url, http_status, categories, datetime_list, author, title, '', text, image_src, [''])

if __name__ == '__main__':

	parse("http://www.esaimaa.fi/vaalit/2015/04/14/Kolumni%3A%20Mit%C3%A4%20tied%C3%A4mme%20p%C3%A4%C3%A4ministerist%C3%A4/2015118896734/478", file('esaimaa.txt', 'w'))
