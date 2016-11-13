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

	article = soup.find( role = 'main' )
	processor.decompose_all( article.find_all( 'script' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'article__section' ), False )
	datetime_list = processor.collect_datetime( article.find( class_ = 'article__published' ), '' )
	author = processor.collect_text( article.find( class_ = 'article__author' ), False )
	title = processor.collect_text( article.find( class_ = 'article__title' ), False )
	ingress = processor.collect_text( article.find( class_ = 'article__summary' ), False )
	text = processor.collect_text( article.find( class_ = 'article__body' ), False )
	images = processor.collect_images_by_parent( article.find_all( class_ = 'article__images' ), '' )
	captions = processor.collect_image_captions( article.find_all( itemprop = 'caption description' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.ksml.fi/uutiset/ulkomaat/kalifornian-ennatyskuivuus-paattyi-rankkasateisiin/1944276", file('keski.txt', 'w'))
