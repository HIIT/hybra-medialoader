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

	article = soup.find( class_ = 'article-content')
	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( class_ = 'related-articles-container' ) )

	categories = [ processor.collect_text( article.find( class_ = 'category' ) )]

	datetime_data = article.find( class_ = 'post-meta' )
	datetime_data.find( class_ = 'category' ).decompose()
	datetime_data.find( class_ = 'updated' ).decompose()
	datetime_data = datetime_data.get_text(' ', strip = True).split(' ')
	datetime_list = [None]
	i = 0
	while i < len(datetime_data) - 1:
		date_string = datetime_data[i]
		time_string = datetime_data[i + 1]
		if len(date_string) < 6:
			date_string = date_string + '2016'
		datetime_object = datetime.strptime( date_string + ' ' + time_string, "%d.%m.%Y %H.%M" )
		datetime_list.append(datetime_object)
		i += 2
	datetime_list.pop(0)
	datetime_list.reverse()

	author = processor.collect_text( article.find( class_ = 'Kirjoittaja') )
	title = processor.collect_text( article.find( class_ = 'Otsikko' ) )
	images = processor.collect_images( article.find_all( 'img' ), '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'caption' ) )

	processor.decompose_all( article.find_all( class_ = 'kuvavaraus-wrapper' ) )

	text = processor.collect_text( article.find( class_ = 'Teksti' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':

	parse("http://www.aamulehti.fi/kotimaa/vanhemmat-uhmaavat-tamperelaisen-koulun-ohjetta-odotetaan-sita-paivaa-etta-joku-jaa-auton-alle/", file('aamulehti.txt', 'w'))
