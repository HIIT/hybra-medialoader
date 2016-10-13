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

	article = soup.find( class_ = 'news-item' )
	processor.decompose_scripts( article )

	category = soup.find( id = 'menu2' ).find( class_ = 'selected' ).get_text( strip = True )
	categories = [str( category.encode('utf8') )]

	datetime_string = article.find( class_ = 'date' ).get_text( strip = True ).replace( ' |Päivitetty: '.decode('utf8'), ',' )
	datetime_data = datetime_string.split( ',' )
	datetime_list = [None]
	for datetime_string in datetime_data:
		datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H:%M' )
		datetime_list.append( datetime_object )
	datetime_list.pop(0)
	datetime_list.reverse()

	author_div = article.find( class_ = 'author' )
	author = author_div.get_text( strip = True )
	author_div.decompose()

	title = article.find( 'h1' ).get_text( ' ', strip = True )
	images = processor.collect_images( article, '', 'http://www.kouvolansanomat.fi' )
	captions = processor.collect_image_captions( article, 'class', 'caption' )

	for img_frame in article.find_all( class_ = 'img_wrapper' ):
		img_frame.decompose()
	text = processor.collect_text( article, 'id', 'main_text' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.kouvolansanomat.fi/vaalit2015/2015/04/14/Ennakko%C3%A4%C3%A4nestys%20vilkkaampaa%20kuin%20edellisiss%C3%A4%20vaaleissa%20%E2%80%94%20kolmasosa%20kouvolalaisista%20on%20jo%20%C3%A4%C3%A4nest%C3%A4nyt/20151430/386", file('kouvolansanomat.txt', 'w'))
