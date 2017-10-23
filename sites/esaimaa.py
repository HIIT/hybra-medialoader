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

	processor.decompose_all( article.find_all( 'blockquote' ) )
	processor.decompose( article.find( class_ = 'sticky-inner-wrapper' ) )

	categories_list = soup.find( class_ = 'breadcrumb' ).find_all( 'li' )[1:-1]
	categories = processor.collect_categories( categories_list )

	datetime_list = processor.collect_datetime( article.find( class_ = 'meta') )

	authors = article.find( class_ = 'authors' )
	author = ''
	for div in authors.find_all( class_ = 'author' ):
		author += processor.collect_text( div.find('p') ) + ','
	author = author[:-1]

	processor.decompose( authors )

	title = processor.collect_text( article.find('h1') )
	ingress = processor.collect_text( article.find( class_ = 'lead' ) )

	images = processor.collect_images( article.find_all( 'img' ), 'src', '' )
	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	processor.decompose( article.find( class_ = 'sticky-outer-wrapper active' ) )
	processor.decompose( article.find('header') )
	processor.decompose( article.find('footer') )

	text = processor.collect_text( article )

	return processor.create_dictionary('Etelä-Saimaa', url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':

	parse("https://esaimaa.fi/uutiset/lahella/2fb49f21-7459-4719-9068-7f5d4bb842ff")
