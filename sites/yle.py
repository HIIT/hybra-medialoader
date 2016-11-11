# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( 'article' )
	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( class_ = 'yle__articlePage__article__author__figure' ) )

	categories = [processor.collect_text( article.find( class_ = 'yle__subject' ), False ).capitalize()]
	datetime_list = processor.collect_datetime( article.find( class_ = 'yle__article__date' ), '' )
	author = processor.collect_text( article.find( class_ = 'yle__articlePage__article__author__name__text' ), False )

	title_div = article.find( class_ = 'yle__article__header__content' )
	title = processor.collect_text( title_div.find( 'h1' ), False )
	ingress = processor.collect_text( title_div.find( 'p' ), False )

	images = processor.collect_images( article.find_all( 'img' ), 'src', 'http:')
	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	processor.decompose_all( article.find_all( 'figcaption' ) )

	text = processor.collect_text( article.find( class_ = 'yle__article__content' ), False )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://yle.fi/uutiset/nordea_synkkyys_jatkuu/7663512", file('yle.txt', 'w'))
