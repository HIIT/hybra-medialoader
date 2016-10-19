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

	article = soup.find( class_ = 'content' )
	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose_all( article.find_all( class_ = 'ad' ) )
	processor.decompose( article.find( id = 'fullWidthBottom' ) )

	categories = [processor.collect_text( article.find( class_ = 'article-category' ) )]

	datetime_object = article.find( 'time' )['datetime'].replace( 'T' , ' ' )
	datetime_object = datetime_object.split( '.' )[0]
	datetime_list = [datetime_object]

	author = processor.collect_text( article.find( class_ = 'author-name' ) )
	title = processor.collect_text( article.find( class_ = 'article-title' ) )
	ingress = processor.collect_text( article.find( class_ = 'lead-paragraph' ) )
	text = processor.collect_text( article.find( class_ = 'editorial' ) )
	images = processor.collect_images( article.find_all( 'img' ), 'http:' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'figcaption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.mtv.fi/uutiset/kotimaa/artikkeli/jarjesto-sipilaan-kohdistuneesta-uhkailusta-iltapaivalehdissa-lausunto-hammastyttaa/4918590", file('mtv.txt', 'w'))
