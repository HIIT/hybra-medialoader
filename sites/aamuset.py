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

	article = soup.find( 'article' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose_all( article.find_all( class_ = 'views-field-field-aamuset-related-images' ) )

	categories_element = soup.find( class_ = 'tsv3-c-as-articletags' )
	categories = processor.collect_categories( categories_element.find_all( 'li' ) )

	datetime_list = processor.collect_datetime( article.find( 'time' ) )

	author = processor.collect_text( article.find( class_  = 'kirjoittaja' ) )
	processor.decompose( article.find( class_  = 'kirjoittaja' ) )

	title = processor.collect_text( article.find( class_ = 'otsikko' ) )
	text = processor.collect_text( article.find( class_ = 'tsv3-c-as-article__textitem--teksti' ) )
	images = processor.collect_images( article.find_all( 'img' ), 'src', 'http://www.aamuset.fi' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'tsv3-c-as-article__attachment__caption' ) )

	return processor.create_dictionary('Aamuset', url, r.status_code, categories, datetime_list, author, title, u'', text, images, captions)

if __name__ == '__main__':

	parse("http://www.aamuset.fi/naista-puhutaan/politiikka/yrttiaho-kanteli-oikeuskanslerille-nato-sopimuksesta", file('aamuset.txt', 'w'))
