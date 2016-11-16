# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( class_ = 'region-content-inner' )
	if article == None:
		return processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])
	
	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose_all( article.find_all( 'noscript' ) )
	processor.decompose( article.find( id = 'comments' ) )
	processor.decompose( article.find( class_ = 'contributor' ) )
	processor.decompose( article.find( class_ = 'field-name-field-author-image' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'field-name-field-category' ), False )
	datetime_list = processor.collect_datetime_objects( article.find_all( class_ = 'date-display-single' ), 'content' )
	author = processor.collect_text( article.find( class_ = 'author-name' ), False )
	title = processor.collect_text( article.find( id = 'page-title' ), False )
	text = processor.collect_text( article.find( class_ = 'field-name-body' ), False )
	images = processor.collect_images( article.find_all( 'img' ), 'src', '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'field-name-field-image-description' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.uusisuomi.fi/kotimaa/79148-ex-ministeri-kummastelee-jotkut-pitavat-lahes-rikollisena", file('uusisuomi.txt', 'w'))
