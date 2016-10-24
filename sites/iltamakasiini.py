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
	processor.decompose( article.find( class_ = 'author' ).find( class_ = 'img' ) )

	categories = [processor.collect_text( article.find( class_ = 'field-name-field-department-tref' ) )]
	datetime_list = processor.collect_datetime( article.find( class_ = 'field-name-post-date' ), '' )
	author = processor.collect_text( article.find( class_ = 'author' ).find( 'h3' ) )
	title = processor.collect_text( article.find( class_ = 'field-name-title' ) )
	text = processor.collect_text( article.find( class_ = 'field field-name-body' ) )
	images = processor.collect_images_by_parent( article.find_all( class_ = 'img' ), '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'caption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':

	parse("http://www.iltamakasiini.fi/artikkeli/279454-kauko-royhkaa-hairikoinyt-rokkari-ehdolla-eduskuntaan", file('iltamakasiini.txt', 'w'))
