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
	processor.decompose_all( article.find_all( class_ = 'nosto' ) )

	categories = [None]
	for category in article.find( class_ = 'links' ).find_all( 'li' ):
		categories.append( processor.collect_text( category ) )
	categories.pop(0)

	datetime_object = article.find( class_ = 'date-display-single' )['content']
	datetime_object = datetime_object.replace( 'T', ' ' ).split( '+' )[0]
	datetime_list = [datetime_object]

	author = processor.collect_text( article.find( class_ = 'tekija' ) )
	title = processor.collect_text( article.find( id = 'page-title' ) )
	text = processor.collect_text( article.find( class_ = 'body' ) )

	images = ['']
	image = article.find( class_ = 'views-field-field-op-main-image' ).find('img')
	if image != None:
		images[0] = str( image['src'].encode('utf8') )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, [''])

if __name__ == '__main__':
	parse("http://www.tiedonantaja.fi/artikkelit/tarinoita-v-kivallasta", file('tiedonantaja.txt', 'w'))
