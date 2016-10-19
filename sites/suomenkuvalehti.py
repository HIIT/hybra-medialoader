# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( class_ = 'article' )
	processor.decompose_all( article.find_all( 'script' ) )

	category_div = article.find( class_ = 'article-category' )
	categories = [None]
	for category in category_div.find_all( 'a' ):
		categories.append( processor.collect_text( category ) )
	categories.pop(0)

	datetime_string = article.find( class_ = 'date' ).get_text( strip = True )
	datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H:%M')
	datetime_list = [datetime_object]

	author = processor.collect_text( article.find( class_ = 'article-credits' ) )
	title = processor.collect_text( article.find( class_ = 'article-title' ) )
	ingress = processor.collect_text( article.find( class_ = 'article-ingress' ) )
	text = processor.collect_text( article.find( class_ = 'article-body' ) )
	images = processor.collect_images_by_parent( article.find_all( class_ = 'fotorama head' ), '')

	captions = [None]
	for caption_div in article.find_all( class_ = 'fotorama head' ):
		caption = BeautifulSoup( caption_div.find( 'a' )['data-caption'], "html.parser" )
		captions.append( processor.collect_text( caption ) )
	captions.pop(0)

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://suomenkuvalehti.fi/jutut/kotimaa/politiikka/timo-soini-aikoo-olla-puheenjohtaja-viela-vuoden-2019-vaaleissa/?shared=74287-e5d264da-500", file('suomenkuvalehti.txt', 'w'))
