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

	article = soup.find( 'article' )
	processor.decompose_scripts( article )
	article.find( class_ = 'author' ).find( class_ = 'img' ).decompose()

	categories = [str( article.find( class_ = 'field-name-field-department-tref' ).get_text( strip = True ).encode('utf8') )]

	datetime_string = article.find( class_ = 'field-name-post-date' ).get_text( strip = True ).replace(' - ', ' ')
	datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H.%M' )
	datetime_list = [datetime_object]

	author = article.find( class_ = 'author' ).find( 'h3' ).get_text( ' ', strip = True )
	title = article.find( class_ = 'field-name-title' ).get_text( ' ', strip = True )
	text = processor.collect_text( article, 'class', 'field field-name-body' )
	images = processor.collect_images( article, 'img', '' )
	captions = processor.collect_image_captions( article, 'class', 'caption' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':

	parse("http://www.iltamakasiini.fi/artikkeli/279454-kauko-royhkaa-hairikoinyt-rokkari-ehdolla-eduskuntaan", file('iltamakasiini.txt', 'w'))
