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

	datetime_list = processor.collect_datetime( article.find( class_ = 'field-name-post-date' ), '' )
	author = article.find( class_ = 'author' )
	processor.decompose( author.find( class_ = 'img' ) )
	author = processor.collect_text( author.find( 'h3' ) )
	title = processor.collect_text( article.find( 'h1' ) )
	text = processor.collect_text( article.find( class_ = 'field field-name-body' ) )
	images = processor.collect_images_by_parent( article.find_all( class_ = 'img' ), '')
	captions = processor.collect_image_captions( article.find_all( class_ = 'caption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':

	parse("http://www.helsinginuutiset.fi/artikkeli/275544-nyt-lentaa-loka-sipila-kerasi-paskalain-turvin-kymmenia-miljoonia", file('helsinginuutiset.txt', 'w'))
