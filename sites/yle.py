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
	article.find( class_ = 'yle__articlePage__article__author__figure' ).decompose()

	category = article.find( class_ = 'yle__subject' ).get_text( strip = True ).capitalize()
	categories = [str( category.encode('utf8') )]

	datetime_data = article.find( class_ = 'yle__article__date' )
	datetime_list = [None]
	for datetime_string in datetime_data.find_all( 'span' ):
		datetime_string = datetime_string.get_text( strip = True )
		datetime_string = datetime_string.replace( 'klo ', '' ).replace( 'päivitetty'.decode('utf8'), '' )
		datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H:%M' )
		datetime_list.append( datetime_object )
	datetime_list.pop(0)
	datetime_list.reverse()

	author = article.find( class_ = 'yle__articlePage__article__author__name' ).get_text( strip = True )

	title_div = article.find( class_ = 'yle__article__header__content' )
	title = title_div.find( 'h1' ).get_text( ' ', strip = True )
	ingress = title_div.find( 'p' ).get_text( ' ', strip = True )
	images = processor.collect_images( article, '', '', 'http:')
	captions = processor.collect_image_captions( article, '', 'figcaption' )

	for caption in article.find_all( 'figcaption' ):
		caption.decompose()

	text = processor.collect_text( article, 'class', 'yle__article__content' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://yle.fi/uutiset/nordea_synkkyys_jatkuu/7663512", file('yle.txt', 'w'))
