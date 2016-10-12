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

	article = soup.find( id = 'main-content' )
	processor.decompose_scripts( article )
	for photographer in article.find_all( class_ = 'photographer' ):
		photographer.decompose()
	article.find( class_ = 'linked-articles' ).decompose()

	categories = [str( article.find( class_ = 'article-category' ).get_text().strip().encode('utf8') )]

	datetime_list = [None]
	datetime_data = article.find_all( 'time' )
	for datetime_string in datetime_data:
		datetime_string = datetime_string.get_text( strip = True ).replace( 'Päivitetty:'.decode('utf8'), '' )
		datetime_object = datetime.strptime( datetime_string.replace(':', '.'), "%d.%m.%Y %H.%M" )
		datetime_list.append(datetime_object)
	datetime_list.pop(0)
	datetime_list.reverse()

	author = article.find( itemprop = 'author creator editor' ).get_text( strip = True )
	title = article.find( 'h1' ).get_text( strip = True )
	ingress = article.find( class_ = 'sub-header' ).get_text( strip = True )
	images = processor.collect_images( article, '' )
	captions = processor.collect_image_captions( article, 'caption' )

	for div in article.find_all( class_ = 'embedded-image' ):
		div.decompose()

	text = processor.collect_text( article, 'class', 'article-text-content' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':

	parse("http://www.hs.fi/paakirjoitukset/a1428030701507", file('hs.txt', 'w'))
