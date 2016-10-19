# -*- coding: utf-8 -*-

import requests
import processor
from bs4 import BeautifulSoup
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( class_ = 'news-item' )
	processor.decompose_all( article.find_all( 'script' ) )

	category = soup.find( id = 'menu2' ).find( class_ = 'selected' ).get_text( strip = True )
	categories = [str( category.encode('utf8') )]

	datetime_string = article.find( class_ = 'date' ).get_text( strip = True )
	datetime_string = datetime_string.replace( ' |Päivitetty: '.decode('utf8'), ',' )
	datetime_string = processor.process( datetime_string )
	datetime_data = datetime_string.split( ',' )
	datetime_list = [None]
	for datetime_string in datetime_data:
		datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H:%M' )
		datetime_list.append( datetime_object )
	datetime_list.pop(0)
	datetime_list.reverse()

	author = article.find( class_ = 'author' ).get_text( strip = True )
	title = article.find( 'h1' ).get_text( strip = True )
	images = processor.collect_images( article, '', '', 'http://www.kymensanomat.fi' )
	captions = processor.collect_image_captions( article, 'class', 'caption')

	for img_frame in article.find_all( class_ = 'img_wrapper' ):
		img_frame.decompose()
	text = processor.collect_text( article, 'id', 'main_text' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.kymensanomat.fi/Online/2015/04/02/Kotkan%20tori%20t%C3%A4yttyi%20vaalipuheista%20ja%20ehdokkaista/2015318855714/4", file('kymeensanomat.txt', 'w'))
