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

	categories = [None]
	categories_data = article.find( class_ = 'field-name-field-department-tref' )
	for category in categories_data.find_all( 'a' ):
		categories.append( str( category.get_text( ' ', strip = True ).encode('utf8') ) )
	categories.pop(0)

	datetime_data = article.find( class_ = 'field-name-post-date' ).get_text().strip().replace(' - ', ' ')
	datetime_object = datetime.strptime( datetime_data, "%d.%m.%Y %H.%M" )
	datetime_list = [datetime_object]

	author = article.find( class_ = 'author' )
	author.find( class_ = 'img' ).decompose()
	author = author.find( 'h3' ).get_text( strip = True )

	title = article.find( 'h1' ).get_text( strip = True )
	text = processor.collect_text( article, 'class', 'field field-name-body' )
	images = processor.collect_images_by_parent( article, 'img', '')
	captions = processor.collect_image_captions( article, 'class', 'caption' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':

	parse("http://www.helsinginuutiset.fi/artikkeli/275544-nyt-lentaa-loka-sipila-kerasi-paskalain-turvin-kymmenia-miljoonia", file('helsinginuutiset.txt', 'w'))
