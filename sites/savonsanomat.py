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

	article = soup.find( role = 'main' )
	processor.decompose_scripts( article )
	article.find( class_ = 'article-author__image' ).decompose()

	category = article.find( class_ = 'article__section' ).get_text( strip = True )
	categories = [str( category.encode('utf8') )]

	datetime_string = article.find( class_ = 'article__published').get_text( strip = True )
	datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H:%M')
	datetime_list = [datetime_object]

	author = article.find( class_ = 'article__author' ).get_text( strip = True )
	title = article.find( class_ = 'article__title' ).get_text( ' ', strip = True )
	text = processor.collect_text( article, 'class', 'article__body' )
	images = processor.collect_images_by_parent( article, 'article__images', '' )
	captions = processor.collect_image_captions( article, '', 'figcaption' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.savonsanomat.fi/uutiset/kotimaa/itsenaisyyspaivan-korkein-kunniamerkki-arkkipiispa-makiselle/1944316", file('savon.txt', 'w'))
