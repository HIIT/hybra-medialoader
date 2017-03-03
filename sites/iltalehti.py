# -*- coding: utf-8 -*-

import requests
import processor
from bs4 import BeautifulSoup
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	r.encoding = 'iso-8859-1'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( id = 'container_keski' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( class_ = 'kp-share-area' ) )

	categories = processor.collect_categories( soup.find_all( class_ = 'sel' ) )
	datetime_list = processor.collect_datetime( article.find( class_ = 'juttuaika' ) )

	author_div = article.find( class_ = 'author' )
	processor.decompose( author_div.find( 'a' ) )
	author = processor.collect_text( author_div, True )

	title = processor.collect_text( article.find( 'h1' ) )
	ingress = processor.collect_text( article.find( class_ = 'ingressi' ), True )
	images = processor.collect_images( article.find_all( 'img' ), 'src', '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'kuvateksti' ) )

	processor.decompose_all( article.find_all( class_ = 'kuvamiddle' ) )

	text = processor.collect_text( article.find( 'isense' ) )

	return processor.create_dictionary('Iltalehti', url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)


def parse_from_archive( url, content ):
	article = BeautifulSoup( content, "html.parser" )

	if article == None:
		return processor.create_dictionary('', url, 404, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	meta = article.find( class_ = 'hakutuloslahde' )

	domain = 'Iltalehti'
	if 'xtra' in meta.text:
		domain += ' Extra'

	datetime_list = processor.collect_datetime( meta )

	category = processor.collect_text( meta ).split(',')[1].strip()
	subcat = processor.collect_text( article.find_all( class_ = 'jalkirivi')[0] )

	categories = []
	for c in [category, subcat]:
		if c:
			categories.append(c)

	author = processor.collect_text( article.find( class_ = 'signeeraus' ) )

	title = processor.collect_text( article.find( class_ = 'otsikko' ) )

	ingress = processor.collect_text( article.find_all( class_ = 'jalkirivi')[1] )
	ingress += ' ' + processor.collect_text( article.find( class_ = 'esirivi' ) )
	ingress = ingress.strip()

	text_divs = article.find_all( class_ = 'artikkelip')
	text = ''
	for text_content in text_divs:
		text += processor.collect_text(text_content) + ' '
	text = text.strip()

	captions = processor.collect_image_captions( article.find_all( class_ = 'kuva') )

	return processor.create_dictionary(domain, url, 200, categories, datetime_list, author, title, ingress, text, [u''], captions)


if __name__ == '__main__':

	parse("http://www.iltalehti.fi/uutiset/2014120218885176_uu.shtml", file('iltalehti.txt', 'w'))
