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

	article = soup.find( class_ = 'content__wrapper' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'typography__category' ) )
	datetime_list = processor.collect_datetime( article.find( class_ = 'meta-content' ) )
	author = processor.collect_text( article.find( class_ = 'typography__author' ) )
	title = processor.collect_text( article.find( class_ = 'content__title' ) )
	ingress = processor.collect_text( article.find( class_ = 'content__intro' ) )
	text = processor.collect_text( article.find( class_ = 'content__body' ) )
	images = processor.collect_images_by_parent( article.find_all( class_ = 'content__main-gallery' ), '')

	captions = [None]
	for caption_div in article.find_all( class_ = 'content__main-gallery' ):
		caption = BeautifulSoup( caption_div.find( 'a' )['data-caption'], "html.parser" )
		captions.append( processor.collect_text( caption ) )
	captions.pop(0)

	return processor.create_dictionary('Suomen kuvalehti', url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://suomenkuvalehti.fi/jutut/kotimaa/politiikka/timo-soini-aikoo-olla-puheenjohtaja-viela-vuoden-2019-vaaleissa/?shared=74287-e5d264da-500", file('suomenkuvalehti.txt', 'w'))
