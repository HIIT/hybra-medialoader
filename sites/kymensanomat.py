# -*- coding: utf-8 -*-

import requests
import processor
from bs4 import BeautifulSoup
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( class_ = 'news-item' )
	processor.decompose_all( article.find_all( 'script' ) )

	menu = soup.find( id = 'menu2' )
	categories = processor.collect_categories( menu.find( class_ = 'selected' ), False )

	datetime_list = processor.collect_datetime( article.find( class_ = 'date' ), '' )
	author = processor.collect_text( article.find( class_ = 'author' ), False )
	title = processor.collect_text( article.find( 'h1' ), False )
	images = processor.collect_images( article.find_all( 'img' ), 'src', 'http://www.kymensanomat.fi' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'caption' ))

	processor.decompose_all( article.find_all( class_ = 'img_wrapper' ) )

	text = processor.collect_text( article.find( id = 'main_text' ), False )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.kymensanomat.fi/Online/2015/04/02/Kotkan%20tori%20t%C3%A4yttyi%20vaalipuheista%20ja%20ehdokkaista/2015318855714/4", file('kymeensanomat.txt', 'w'))
