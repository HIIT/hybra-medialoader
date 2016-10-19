# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime
import time

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( 'article' )
	processor.decompose_all( article.find_all( 'script' ) )

	category = article.find( class_ = 'article-release-info__section' ).get_text( strip = True )
	categories = [str( category.encode('utf8') )]

	datetime_string = article.find( class_ = 'article-release-info__time' ).get_text( strip = True )
	if len( datetime_string ) > 5:
		datetime_object = datetime.date( datetime.strptime( datetime_string, '%d.%m.%Y' ) )
	else:
		datetime_string = time.strftime( '%d.%m.%Y' ) + ' ' + datetime_string
		datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H:%M' )
	datetime_list = [datetime_object]

	author = article.find( itemprop = 'author' ).get_text( strip = True )

	title_div = article.find( class_ = 'article-single-heading' )
	title = title_div.find( 'h1' ).get_text( ' ', strip = True )
	ingress = title_div.find( 'p' ).get_text( ' ', strip = True )

	text = processor.collect_text( article, 'class', 'article-single-section__content' )
	images = processor.collect_images( article, '', '', 'http://www.maaseuduntulevaisuus.fi' )
	captions = processor.collect_image_captions( article, '', 'figcaption' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.maaseuduntulevaisuus.fi/maatalous/nurmipelloille-voi-tulla-k%C3%A4ytt%C3%B6rajoituksia-1.76216", file('maaseudun.txt', 'w'))
