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

	article = soup.find( role = 'main' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'article__section' ) )
	datetime_list = processor.collect_datetime( article.find( class_ = 'article__published' ) )
	author = processor.collect_text( article.find( class_ = 'article__author' ) )
	title = processor.collect_text( article.find( class_ = 'article__title' ) )
	ingress = processor.collect_text( article.find( class_ = 'article__summary' ) )
	text = processor.collect_text( article.find( class_ = 'article__body' ) )
	images = processor.collect_images_by_parent( article.find_all( class_ = 'article__images' ), '' )
	captions = processor.collect_image_captions( article.find_all( itemprop = 'caption description' ) )

	return processor.create_dictionary('Keskisuomalainen', url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)


def parse_from_archive(url, content):
	article = BeautifulSoup( content, "html.parser" )

	if article == None:
		return processor.create_dictionary('', url, 404, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )

	meta = article.find( class_ = 'date' )

	categories = [processor.collect_text(meta).split(' ')[0]]
	datetime_list = str(processor.collect_datetime( meta ))
	author = processor.collect_text( article.find( class_  = 'author'), True )

	processor.decompose( meta )

	title_parts = article.find_all('h2')
	title = ''
	for part in title_parts:
		title += processor.collect_text(part, True) + ' '
	title = title.strip()

	ingress_parts = article.find_all('h4')
	ingress = ''
	for part in ingress_parts:
		ingress += processor.collect_text(part, True) + ' '
	ingress = ingress.strip()

	processor.decompose( article.find_all( 'p' )[-1] )

	text = processor.collect_text( article )

	return processor.create_dictionary('Keskisuomalainen', url, 200, categories, datetime_list, author, title, ingress, text, [u''], [u''])


if __name__ == '__main__':
	parse("http://www.ksml.fi/uutiset/ulkomaat/kalifornian-ennatyskuivuus-paattyi-rankkasateisiin/1944276", file('keski.txt', 'w'))
