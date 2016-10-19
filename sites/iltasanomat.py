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

	article = soup.find( class_ = 'single-article' )

	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose_all( article.find_all( class_ = 'print-url' ) )

	category = url.split('/')[3]
	categories = [category.capitalize().encode('utf8')]

	datetime_string = article.find( itemprop = 'datePublished' ).get_text( strip = True ).replace('Julkaistu:', '')
	datetime_data = datetime_string.split( ' ' )
	if len( datetime_data[0] ) < 7:
		datetime_data[0] = datetime_data[0] + '2016'
	datetime_object = datetime.strptime( datetime_data[0] + ' ' + datetime_data[1], '%d.%m.%Y %H:%M')
	datetime_list = [datetime_object]

	author = processor.collect_text( article.find( itemprop = 'author' ) )
	title = processor.collect_text( article.find( 'h1' ) )
	ingress = processor.collect_text( article.find( class_ = 'ingress' ) )
	text = processor.collect_text( article.find( class_ = 'body' ) )
	images = processor.collect_images( article.find_all( 'img' ), '')
	captions = processor.collect_image_captions( article.find_all( itemprop = 'caption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.iltasanomat.fi/ulkomaat/art-1288789081654.html", file('iltasa.txt', 'w'))
