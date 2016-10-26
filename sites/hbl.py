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

	article = soup.find( class_ = 'article-body' )
	processor.decompose_all( article.find_all( 'script' ) )

	departments = article.find( class_ = 'departments' )
	categories = processor.collect_categories( departments.find_all( 'a' ), False )
	datetime_list = processor.collect_datetime_objects( article.find_all( 'time' ), 'datetime' )
	author = processor.collect_text( article.find( class_ = 'author' ), False )
	title = processor.collect_text( article.find( 'h1' ), False )
	ingress = processor.collect_text( article.find( class_ = 'ingress' ), False )

	# This does not get the text because HBL demands registration
	text = processor.collect_text( article.find( class_ = 'text' ), False )

	images = processor.collect_images( article.find_all( 'img' ), 'src', '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'ksf-image-meta' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':

	parse("http://hbl.fi/nyheter/2014-12-03/690266/hawking-ai-kan-vara-slutet-oss", file('hbl.txt', 'w'))
