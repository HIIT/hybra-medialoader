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

	article = soup.find( class_ = 'article-content' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )

	meta = article.find( class_ = 'post-meta' )

	categories = processor.collect_categories( meta.find_all( class_ = 'category' ), True )
	datetime_list = processor.collect_datetime( meta )
	author = processor.collect_text( article.find( class_ = 'author--main' ) )
	title = processor.collect_text( article.find( class_ = 'heading--main' ) )
	text = processor.collect_text( article.find( class_ = 'content--main' ) )
	images = processor.collect_images( article.find_all( 'img' ), 'src', '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'caption' ) )

	return processor.create_dictionary('Satakunnan kansa', url, r.status_code, categories, datetime_list, author, title, u'', text, images, captions)

def parse_from_archive(url, content):
	article = BeautifulSoup( content, "html.parser" )

	if article == None:
		return processor.create_dictionary('Satakunnan kansa', url, 404, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	meta = article.find( class_ = 'hakutuloslahde' )

	datetime_list = processor.collect_datetime( meta )

	category = processor.collect_text( meta ).split(',')[1].strip()
	subcat = processor.collect_text( article.find( class_ = 'jalkirivi' ) )

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
	text = processor.process( text.strip() )
	text += processor.collect_text( article.find( class_ = 'korjaus' ) )

	captions = processor.collect_image_captions( article.find_all( class_ = 'kuva') )

	return processor.create_dictionary('Satakunnan kansa', url, 200, categories, datetime_list, author, title, ingress, text, [u''], captions)


if __name__ == '__main__':
	parse("http://www.satakunnankansa.fi/Satakunta/1194972499877/artikkeli/myrsky+runteli+myos+vaalimainoksia.html", file('satakunnankansa.txt', 'w'))
