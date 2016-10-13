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

	article = soup.find( class_ = 'article' )
	processor.decompose_scripts( article )

	categories = processor.collect_categories_nav( soup, 'active' )

	datetime_list = [None]
	datetime_data = article.find( class_ = 'date' ).get_text( ' ', strip = True )
	datetime_data = datetime_data.replace( ' (Päivitetty: '.decode('utf8'), ',' ).replace( ')', '' ).replace( ':', '.' )
	datetime_data = datetime_data.split(',')
	for datetime_string in datetime_data:
		datetime_object = datetime.strptime( datetime_string, "%d.%m.%Y %H.%M" )
		datetime_list.append(datetime_object)
	datetime_list.pop(0)
	datetime_list.reverse()

	title = article.find( class_ = 'newsHeadline' ).get_text( ' ', strip = True )
	ingress = article.find( class_ = 'lead').get_text( ' ', strip = True )
	text = processor.collect_text( article, 'class', 'articleBody' )
	images = processor.collect_images( article, '', 'http://www.ilkka.fi' )
	captions = processor.collect_image_captions( article, 'class', 'newsImgText' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, '', title, ingress, text, images, captions)

if __name__ == '__main__':

	parse( 'http://www.ilkka.fi/uutiset/kotimaa/vertailu-suomessa-kolmanneksi-vahiten-korruptiota-1.1731397', file('ilkka.txt', 'w') )
