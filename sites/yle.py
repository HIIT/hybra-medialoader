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
	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( class_ = 'yle__articlePage__article__author__figure' ) )

	categories = [processor.collect_text( article.find( class_ = 'yle__subject' ) ).capitalize()]

	datetime_data = article.find( class_ = 'yle__article__date' )
	datetime_list = [None]
	for datetime_string in datetime_data.find_all( 'span' ):
		datetime_string = datetime_string.get_text( strip = True )
		datetime_string = datetime_string.replace( 'klo ', '' ).replace( 'päivitetty'.decode('utf8'), '' )
		datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H:%M' )
		datetime_list.append( datetime_object )
	datetime_list.pop(0)
	datetime_list.reverse()

	author = processor.collect_text( article.find( class_ = 'yle__articlePage__article__author__name' ) )

	title_div = article.find( class_ = 'yle__article__header__content' )
	title = processor.collect_text( title_div.find( 'h1' ) )
	ingress = processor.collect_text( title_div.find( 'p' ) )

	images = processor.collect_images( article.find_all( 'img' ), 'http:')
	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	processor.decompose_all( article.find_all( 'figcaption' ) )

	text = processor.collect_text( article.find( class_ = 'yle__article__content' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://yle.fi/uutiset/nordea_synkkyys_jatkuu/7663512", file('yle.txt', 'w'))
