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

	article = soup.find( 'main' )
	processor.decompose_all( article.find_all( 'script' ) )
	for quote in article.find_all( class_ = 'nosto' ):
		quote.decompose()

	categories = [None]
	for category in article.find( class_ = 'links' ).find_all( 'li' ):
		categories.append( str( category.get_text( strip = True ).encode('utf8') ) )
	categories.pop(0)

	datetime_object = article.find( class_ = 'date-display-single' )['content']
	datetime_object = datetime_object.replace( 'T', ' ' ).split( '+' )[0]
	datetime_list = [datetime_object]

	author = article.find( class_ = 'tekija' ).get_text( strip = True )
	title = article.find( id = 'page-title' ).get_text( strip = True )
	text = processor.collect_text( article, 'class', 'body' )

	images = ['']
	image = article.find( class_ = 'views-field-field-op-main-image' ).find('img')
	if image != None:
		images[0] = str( image['src'].encode('utf8') )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, [''])

if __name__ == '__main__':
	parse("http://www.tiedonantaja.fi/artikkelit/tarinoita-v-kivallasta", file('tiedonantaja.txt', 'w'))
