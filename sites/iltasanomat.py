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
	for print_url in article.find_all( class_ = 'print-url' ):
		print_url.decompose()

	category = url.split('/')[3]
	categories = [str( category.capitalize().encode('utf8') )]

	datetime_string = article.find( itemprop = 'datePublished' ).get_text( strip = True ).replace('Julkaistu:', '')
	datetime_data = datetime_string.split( ' ' )
	if len( datetime_data[0] ) < 7:
		datetime_data[0] = datetime_data[0] + '2016'
	datetime_object = datetime.strptime( datetime_data[0] + ' ' + datetime_data[1], '%d.%m.%Y %H:%M')
	datetime_list = [datetime_object]

	author = article.find( itemprop = 'author' ).get_text( strip = True )
	title = article.find( 'h1' ).get_text( ' ', strip = True )
	ingress = article.find( class_ = 'ingress' ).get_text(' ', strip = True)
	text = processor.collect_text( article, 'class', 'body' )
	images = processor.collect_images( article, '', '', '')
	captions = processor.collect_image_captions( article, 'itemprop', 'caption' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.iltasanomat.fi/ulkomaat/art-1288789081654.html", file('iltasa.txt', 'w'))
