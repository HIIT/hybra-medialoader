# -*- coding: utf-8 -*-

import requests
import processor
from bs4 import BeautifulSoup
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	r.encoding = 'iso-8859-1'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( id = 'container_keski' )
	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( class_ = 'kp-share-area' ) )

	categories = processor.collect_categories( soup.find_all( class_ = 'sel' ), False )
	datetime_list = processor.collect_datetime( article.find( class_ = 'juttuaika' ), '' )

	author_div = article.find( class_ = 'author' )
	processor.decompose( author_div.find( 'a' ) )
	author = processor.collect_text( author_div, True )

	title = processor.collect_text( article.find( 'h1' ), False )
	ingress = processor.collect_text( article.find( class_ = 'ingressi' ), True )
	images = processor.collect_images( article.find_all( 'img' ), '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'kuvateksti' ) )

	processor.decompose_all( article.find_all( class_ = 'kuvamiddle' ) )

	text = processor.collect_text( article.find( 'isense' ), False )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':

	parse("http://www.iltalehti.fi/uutiset/2014120218885176_uu.shtml", file('iltalehti.txt', 'w'))
