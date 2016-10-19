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

	article = soup.find( class_ = 'full-article' )
	processor.decompose_all( article.find_all( 'script' ) )

	category = article.find( class_ = 'meta-category' ).get_text( strip = True )
	categories = [str( category.encode('utf8') )]

	datetime_list = [None]
	for datetime_string in article.find_all( 'time' ):
		datetime_string = datetime_string.get_text( strip = True )
		datetime_string = datetime_string.replace( 'klo ', '')
		datetime_string = datetime_string.replace( '(päivitetty '.decode('utf8'), '' ).replace( ')', '' )
		datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H:%M')
		datetime_list.append( datetime_object )
	datetime_list.pop(0)
	datetime_list.reverse()

	author = article.find( itemprop = 'author' ).get_text( strip = True )
	title = article.find( itemprop = 'name headline' ).get_text( ' ', strip = True )
	ingress = article.find( class_ = 'ingress' ).get_text( ' ', strip = True )

	images = [None]
	for img in article.find_all( 'img' ):
		images.append( '' + str( img['data-src'].encode('utf8') ) )
	images.pop(0)

	captions = processor.collect_image_captions( article, '', 'figcaption' )

	for slides in article.find_all( class_ ='flexslider'):
		slides.decompose()

	text = processor.collect_text( article, 'class', 'articlepart-1' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.verkkouutiset.fi/talous/ammattisijoittajan_neuvot-33352", file('verkkouutiset.txt', 'w'))
