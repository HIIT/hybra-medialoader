# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( class_ = 'news-item')
	processor.decompose_scripts( article )

	menu = soup.find( id = 'menu2' )
	category = menu.find( class_ = 'selected' ).get_text(strip = True)
	categories = [str( category.encode('utf8') )]

	datetime_data = article.find( class_ = 'date').get_text(' ', strip = True)
	datetime_list = [datetime.strptime( datetime_data, "%d.%m.%Y %H:%M" )]

	author = article.find_all( class_ = 'lahde' )
	author = author[0].get_text(' ', strip = True) + ' ' + author[1].get_text(' ', strip = True)
	for div in article.find_all( 'div', {'class' : 'lahde'} ):
		div.decompose()

	title = article.find('h1').get_text(strip = True)
	text = processor.collect_text( article, 'id', 'main_text' )
	images = processor.collect_images( article, 'http://www.esaimaa.fi' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, [''])

if __name__ == '__main__':

	parse("http://www.esaimaa.fi/vaalit/2015/04/14/Kolumni%3A%20Mit%C3%A4%20tied%C3%A4mme%20p%C3%A4%C3%A4ministerist%C3%A4/2015118896734/478", file('esaimaa.txt', 'w'))
