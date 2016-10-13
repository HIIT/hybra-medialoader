# -*- coding: utf-8 -*-

import requests
import processor
from bs4 import BeautifulSoup
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return

	r.encoding = 'iso-8859-1'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( id = 'container_keski' )
	processor.decompose_scripts( article )
	article.find( class_ = 'kp-share-area' ).decompose()

	categories = processor.collect_categories_nav( soup, 'sel' )

	datetime_data = article.find( class_ = 'juttuaika' ).get_text( strip = True ).split( ' ' )
	datetime_object = datetime.strptime( datetime_data[1] + ' ' + datetime_data[3], "%d.%m.%Y %H.%M" )
	datetime_list = [datetime_object]

	author_div = article.find( class_ = 'author' )
	author_div.find( 'a' ).decompose()
	author = '' + author_div.get_text( ' ', strip = True )
	author_div.decompose()

	title = article.find( 'h1' ).get_text( ' ', strip = True )

	ingress_tag = article.find( class_ = 'ingressi' )
	ingress = ingress_tag.get_text( ' ', strip = True )
	ingress_tag.decompose()

	images = processor.collect_images( article, '', '' )
	captions = processor.collect_image_captions( article, 'class', 'kuvateksti' )
	for img in article.find_all( class_ = 'kuvamiddle' ):
		img.decompose()

	text = processor.collect_text( article, 'isense', '' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':

	parse("http://www.iltalehti.fi/uutiset/2014120218885176_uu.shtml", file('iltalehti.txt', 'w'))
