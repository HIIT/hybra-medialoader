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

	article = soup.find( class_ = 'view-news-item')
	processor.decompose_scripts( article )
	for img in article.find_all( class_ = 'views-field-field-aamuset-related-images' ):
		img.decompose()

	categories = [str( article.find( class_ = 'views-field-field-aamuset-category').get_text().strip() ).encode('utf8')]

	datetime_data = article.find( class_ = 'views-field-field-aamuset-category').parent.find_all('div')[3]
	datetime_data = datetime_data.get_text(' ', strip = True)
	datetime_data = datetime_data.replace(')', '').split(' ')
	if len( datetime_data ) > 2:
		datetime_data.pop(2)
	datetime_list = [None]
	i = 0
	while i < len(datetime_data) - 1:
		date_string = datetime_data[i]
		time_string = datetime_data[i + 1]
		datetime_object = datetime.strptime( date_string + ' ' + time_string, "%d.%m.%Y %H:%M" )
		datetime_list.append(datetime_object)
		i += 2
	datetime_list.pop(0)
	datetime_list.reverse()

	author = article.find( class_  = 'views-field-field-visiting-journalist' ).get_text().strip()
	title = article.find( class_ = 'views-field-title' ).get_text().strip()
	text = processor.collect_text( article, 'class', 'views-field views-field-body' )
	images = processor.collect_images( article, '', '', '' )
	captions = processor.collect_image_captions( article, 'class', 'views-field-field-aamuset-caption-1' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':

	parse("http://www.aamuset.fi/naista-puhutaan/politiikka/yrttiaho-kanteli-oikeuskanslerille-nato-sopimuksesta", file('aamuset.txt', 'w'))
