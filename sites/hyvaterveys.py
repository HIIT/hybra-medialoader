# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( 'article' )
	processor.decompose_scripts( article )
	article.find( class_ = 'region bottom' ).decompose()

	categories = [str( article.find( class_ = 'field-name-field-category' ).get_text( strip = True ) )]

	datetime_string = article.find( class_ = 'field-name-post-date' ).get_text( strip = True )
	datetime_string = datetime_string.replace( 'klo ', '').replace( ' | ', ' ' ).replace( ':', '.' )
	datetime_data = datetime_string.split( ' ' )
	datetime_object = datetime.strptime( datetime_data[1] + ' ' + datetime_data[0], "%d.%m.%Y %H.%M" )
	datetime_list = [datetime_object]

	author = article.find( class_ = 'field-name-field-author' ).get_text( strip = True )
	title = article.find( 'h1' ).get_text( strip = True )
	ingress = article.find( class_ = 'field-name-field-summary' ).get_text( strip = True )
	text = processor.collect_text( article, 'class', 'field-name-field-body' )
	images = processor.collect_images( article, '')
	captions = processor.collect_image_captions( article, 'file-image-description-caption' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':

	parse("http://www.hyvaterveys.fi/artikkeli/blogit/paljain_jaloin_pariisissa/eriavien_mielipiteiden_merkityksesta", file('hyvaterveys.txt', 'w'))
