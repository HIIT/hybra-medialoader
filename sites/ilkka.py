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

	article = soup.find( class_ = 'article' )
	processor.decompose_scripts( article )

	categories = [None]
	categories_data = soup.find_all( class_ = 'active' )
	for category in categories_data:
		categories.append( str( category.get_text( strip = True ).encode('utf8') ) )
	categories.pop(0)

	datetime_string = article.find( class_ = 'date' ).get_text( strip = True ).replace( ':', '.' )
	datetime_object = datetime.strptime( datetime_string, "%d.%m.%Y %H.%M" )
	datetime_list = [datetime_object]

	title = article.find( class_ = 'newsHeadline' ).get_text( ' ', strip = True )
	ingress = article.find( class_ = 'lead').get_text( ' ', strip = True )
	text = processor.collect_text( article, 'class', 'articleBody' )
	images = processor.collect_images( article, 'http://www.ilkka.fi' )
	captions = processor.collect_image_captions( article, 'newsImgText' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, '', title, ingress, text, images, captions)

if __name__ == '__main__':

	parse( 'http://www.ilkka.fi/uutiset/kotimaa/vertailu-suomessa-kolmanneksi-vahiten-korruptiota-1.1731397', file('ilkka.txt', 'w') )
