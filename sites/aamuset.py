# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( class_ = 'view-news-item')
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose_all( article.find_all( class_ = 'views-field-field-aamuset-related-images' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'views-field-field-aamuset-category') )
	datetime_list = processor.collect_datetime( article.find( class_ = 'views-field-field-aamuset-category').parent.find_all('div')[3] )
	author = processor.collect_text( article.find( class_  = 'views-field-field-visiting-journalist' ) )
	title = processor.collect_text( article.find( class_ = 'views-field-title' ) )
	text = processor.collect_text( article.find( class_ = 'views-field views-field-body' ) )
	images = processor.collect_images( article.find_all( 'img' ), 'src', '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'views-field-field-aamuset-caption-1' ) )

	return processor.create_dictionary('Aamuset', url, r.status_code, categories, datetime_list, author, title, u'', text, images, captions)

if __name__ == '__main__':

	parse("http://www.aamuset.fi/naista-puhutaan/politiikka/yrttiaho-kanteli-oikeuskanslerille-nato-sopimuksesta", file('aamuset.txt', 'w'))
