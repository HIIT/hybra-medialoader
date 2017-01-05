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

	article = soup.find( class_ = 'single-article' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])


	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose_all( article.find_all( class_ = 'print-url' ) )

	category = url.split('/')[3]
	categories = [category.capitalize().encode('utf8')]

	datetime_list = processor.collect_datetime( article.find( itemprop = 'datePublished' ), '' )
	author = processor.collect_text( article.find( itemprop = 'author' ), False )
	title = processor.collect_text( article.find( 'h1' ), False )
	ingress = processor.collect_text( article.find( class_ = 'ingress' ), False )
	text = processor.collect_text( article.find( class_ = 'body' ), False )
	images = processor.collect_images( article.find_all( 'img' ), 'src', '')
	captions = processor.collect_image_captions( article.find_all( itemprop = 'caption' ) )

	return processor.create_dictionary('Iltasanomat', url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.iltasanomat.fi/ulkomaat/art-1288789081654.html", file('iltasa.txt', 'w'))
