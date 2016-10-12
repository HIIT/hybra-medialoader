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

	article = soup.find( class_ = 'article-body' )
	for script in article.find_all( 'script' ):
		script.decompose()

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

	text = article.find( class_ = 'text' ).get_text( ' ', strip = True ) # Does not get the text. Possibly because HBL demands sign in?
	text = processor.process(text)

	images = article.find_all( 'img' )
	image_src = [None]
	for img in images:
		image_src.append( str( img['src'].encode('utf8') ) )
	image_src.pop(0)

	captions = article.find_all( class_ = 'ksf-image-meta' )
	captions_text = [None]
	for caption in captions:
		captions_text.append( str( caption.get_text( ' ', strip = True).encode('utf8') ) )
	captions_text.pop(0)

	return processor.create_dictionary(url, http_status, categories, datetime_list, author, title, ingress, text, image_src, captions_text)

if __name__ == '__main__':

	parse("http://hbl.fi/nyheter/2014-12-03/690266/hawking-ai-kan-vara-slutet-oss", file('hbl.txt', 'w'))
