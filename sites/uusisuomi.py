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

	article = soup.find( class_ = 'region-content-inner' )
	processor.decompose_scripts( article )
	processor.decompose_noscripts( article )
	article.find( id = 'comments' ).decompose()
	article.find( class_ = 'contributor' ).decompose()
	article.find( class_ = 'field-name-field-author-image' ).decompose()

	category = article.find( class_ = 'field-name-field-category' ).get_text( strip = True )
	categories = [str( category.encode('utf8') )]

	datetime_object = article.find( class_ = 'date-display-single' )['content']
	datetime_object = datetime_object.replace( 'T', ' ' ).split( '+' )[0]
	datetime_list = [datetime_object]

	author = article.find( class_ = 'author-name' ).get_text( strip = True )
	title = article.find( id = 'page-title' ).get_text( strip = True )
	text = processor.collect_text( article, 'class', 'field-name-body' )
	images = processor.collect_images( article, '', '', '' )
	captions = processor.collect_image_captions( article, 'class', 'field-name-field-image-description' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.uusisuomi.fi/kotimaa/79148-ex-ministeri-kummastelee-jotkut-pitavat-lahes-rikollisena", file('uusisuomi.txt', 'w'))
