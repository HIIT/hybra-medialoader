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

	article = soup.find( id = 'main-content' )

	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose_all( article.find_all( class_ = 'photographer' ) )
	processor.decompose( article.find( class_ = 'linked-articles' ) )

	categories = [processor.collect_text( article.find( class_ = 'article-category' ) )]

	datetime_list = [None]
	datetime_data = article.find_all( 'time' )
	for datetime_string in datetime_data:
		datetime_string = datetime_string.get_text( strip = True ).replace( 'Päivitetty:'.decode('utf8'), '' )
		datetime_object = datetime.strptime( datetime_string.replace(':', '.'), "%d.%m.%Y %H.%M" )
		datetime_list.append(datetime_object)
	datetime_list.pop(0)
	datetime_list.reverse()

	author = processor.collect_text( article.find( itemprop = 'author creator editor' ) )
	title = processor.collect_text( article.find( 'h1' ) )
	ingress = processor.collect_text( article.find( class_ = 'sub-header' ) )
	images = processor.collect_images( article.find_all( 'img' ), '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'caption' ) )

	processor.decompose_all( article.find_all( class_ = 'embedded-image' ) )

	text = processor.collect_text( article.find( class_ = 'article-text-content' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':

	parse("http://www.hs.fi/paakirjoitukset/a1428030701507", file('hs.txt', 'w'))
