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
	processor.decompose_all( article.find_all( class_ = 'somebar' ) )
	processor.decompose( article.find( class_ = 'tags' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'post-category' ), False )

	datetime_string = article.find( class_ = 'timestamp' ).get_text( ' ', strip = True )
	datetime_string = processor.convert_month( datetime_string.replace( ',', '' ) )
	datetime_list = [datetime.strptime( datetime_string, '%m %d %Y %H:%M' )]

	author = processor.collect_text( article.find( class_ = 'article-page-writer' ), True )
	title = processor.collect_text( article.find( class_ = 'post-title' ), False )
	text = processor.collect_text( article.find( class_ = 'post-content' ), False )
	images = processor.collect_images( article.find_all( 'img' ), 'src', '' )
	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	return processor.create_dictionary('Suomen uutiset', url, r.status_code, categories, datetime_list, author, title, u'', text, images, captions)

if __name__ == '__main__':
	parse("https://www.suomenuutiset.fi/perussuomalaiset-hurjassa-nosteessa-puoluesihteeri-ei-yllattynyt/", file('suomenuutiset.txt', 'w'))
