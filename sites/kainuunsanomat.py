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

	article = soup.find( 'article' )
	processor.decompose_scripts( article )
	for img in article.find_all( class_ = 'attImage' ):
		img.decompose()

	meta = article.find( 'time' )

	category = meta.find( 'b' )
	categories = [str( category.get_text( strip = True ).encode('utf8') )]
	category.decompose()

	datetime_string = meta.get_text( strip = True ).replace( 'Julkaistu ', '' ).replace( 'klo ', '' )
	datetime_data = datetime_string.split( '\t' )
	datetime_object = datetime.strptime( datetime_data[0], '%d.%m.%Y %H:%M' )
	datetime_list = [datetime_object]

	author_tag = article.find( class_ = 'Kirjoittaja' )
	author = author_tag.get_text( strip = True )
	author_tag.decompose()

	title = article.find( 'h1' ).get_text( ' ', strip = True )
	ingress = article.find( class_ = 'Alaotsikko' ).get_text( ' ', strip = True )
	text = processor.collect_text( article, 'class', 'Teksti')
	images = processor.collect_images( article, '', '', '' )
	captions = processor.collect_image_captions( article, 'class', 'featuredCaption' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.kainuunsanomat.fi/kainuun-sanomat/kotimaa/lipponen-moitti-sipilan-puheita-ministerien-vahentamisesta/", file('kainuunsanomat.txt', 'w'))
