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
	processor.decompose( article.find( class_ = 'region bottom' ) )
	processor.decompose( article.find( class_ = 'field-name-field-related-content' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'field-name-field-category' ) )
	datetime_list = processor.collect_datetime( article.find( class_ = 'field-name-post-date' ), 'timedate' )
	author = processor.collect_text( article.find( class_ = 'field-name-field-author' ) )
	title = processor.collect_text( article.find( 'h1' ) )
	ingress = processor.collect_text( article.find( class_ = 'field-name-field-summary' ) )
	text = processor.collect_text( article.find( class_ = 'field-name-field-body' ) )

	images = []
	for img in processor.collect_images( article.find_all( 'img' ), 'src', ''):
		if 'placeholder' not in img:
			images.append(img)

	captions = processor.collect_image_captions( article.find_all( class_ = 'file-image-description-caption' ) )

	return processor.create_dictionary('Hyvä terveys', url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':

	parse("http://www.hyvaterveys.fi/artikkeli/blogit/paljain_jaloin_pariisissa/eriavien_mielipiteiden_merkityksesta", file('hyvaterveys.txt', 'w'))
