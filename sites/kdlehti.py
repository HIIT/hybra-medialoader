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

	article = soup.find( 'article' )
	processor.decompose_all( article.find_all( 'script' ) )
	for img in article.find( 'header' ).find_all( 'img' ):
		img.decompose()
	for quote in article.find_all( 'blockquote' ):
		quote.decompose()

	category = article.find( class_ = 'cat' ).get_text( strip = True )
	categories = [str( category.encode('utf8') )]

	datetime_string = article.find( class_ = 'date' ).get_text( strip = True ).replace( 'klo ', ' ')
	datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H:%M' )
	datetime_list = [datetime_object]

	author = article.find( class_ = 'author' ).get_text( strip = True )
	title = article.find( class_ = 'article-title' ).get_text( strip = True )

	ingress_tag = article.find( class_ = 'ingress' )
	ingress = ingress_tag.get_text( strip = True )
	ingress_tag.decompose()

	text = processor.collect_text( article, 'class', 'content' )
	images = processor.collect_images( article, '', '', 'http:' )

	captions = [None]
	for img_frame in article.find_all( class_ = 'featured-image' ):
		captions.append( str( img_frame.get_text( ' ', strip = True ).encode('utf8') ) )
	captions.pop(0)

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.kdlehti.fi/2015/03/15/paivi-rasanen-internetin-terrorismisisaltoon-puututtava-tehokkaammin/", file('kdlehti.txt', 'w'))
