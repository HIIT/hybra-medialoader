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

	article = soup.find( class_ = 'article-body' )
	processor.decompose_all( article.find_all( 'script' ) )

	categories = [None]
	categories_data = article.find( class_ = 'departments' )
	for category in categories_data.find_all( 'a' ):
		categories.append( str( category.get_text( ' ', strip = True ).encode('utf8') ) )
	categories.pop(0)

	datetime_data = article.find( 'time' ).get_text().strip().replace(':', '.')
	datetime_object = datetime.strptime( datetime_data, "%d.%m.%Y %H.%M" )
	datetime_list = [datetime_object]

	author = article.find( class_ = 'author' ).get_text( strip = True )
	title = article.find( 'h1' ).get_text( strip = True )
	ingress = article.find( class_ = 'ingress' ).get_text( strip = True )
	text = processor.collect_text( article, 'class', 'text') # Does not get the text because HBL demands registration
	images = processor.collect_images( article, '', '', '' )
	captions = processor.collect_image_captions( article, 'class', 'ksf-image-meta' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':

	parse("http://hbl.fi/nyheter/2014-12-03/690266/hawking-ai-kan-vara-slutet-oss", file('hbl.txt', 'w'))
