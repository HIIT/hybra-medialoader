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

	meta = article.find( class_ = 'tsv3-c-common-article__meta__row1' )

	category = meta.find( 'a' ).get_text( strip = True )
	categories = [str( category.encode('utf8') )]

	datetime_object = meta.find( 'time' )['datetime']
	datetime_object = datetime_object.split( '+' )[0]
	datetime_list = [datetime_object]

	author = ''
	if article.find( class_ = 'kirjoittaja' ) != None:
		author = author.get_text( strip = True )

	title = article.find( class_ = 'otsikko' ).get_text( ' ', strip = True)
	text = processor.collect_text( article, 'class', 'tsv3-c-common-article__textitem tsv3-c-common-article__textitem--teksti')
	images = processor.collect_images( article, '', '', 'http://www.ts.fi' )
	captions = processor.collect_image_captions( article, 'class', 'tsv3-c-common-article__attachment__info__caption' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.ts.fi/eduskuntavaalit/750980/Start+up+yrittaja+kuplii+innostusta", file('ts.txt', 'w'))
