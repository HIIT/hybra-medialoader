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
	processor.decompose_scripts( article )
	article.find( 'footer' ).decompose()
	for ad in article.find_all( class_ = 'cb-module-title' ):
		ad.decompose()
	for quote in article.find_all( 'blockquote' ):
		quote.decompose()

	categories =  [None]
	for category in article.find_all( class_ = 'cb-category' ):
		categories.append( str( category.get_text( strip = True ).encode('utf8') ) )
	categories.pop(0)

	datetime_list = [None]
	for time in article.find_all( 'time' ):
		datetime_string = time.get_text( strip = True )
		datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H.%M' )
		datetime_list.append( datetime_object )
	datetime_list.pop(0)
	datetime_list.reverse()

	author = article.find( class_ = 'cb-author' ).get_text( strip = True )
	title = article.find( class_ = 'entry-title' ).get_text( strip = True )

	ingress_tag = article.find( class_ = 'cb-entry-content' ).find( 'h4' )
	ingress = ingress_tag.get_text( strip = True )
	ingress_tag.decompose()

	text = processor.collect_text( article, 'class', 'cb-entry-content')
	images = processor.collect_images( article, '', '' )
	captions = processor.collect_image_captions( article, 'class', 'caption' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.kansanuutiset.fi/kulttuuri/kirjat/3341821/lahi-idan-rajoja-vedetaan-uusiksi", file('kansanuutiset.txt', 'w'))
