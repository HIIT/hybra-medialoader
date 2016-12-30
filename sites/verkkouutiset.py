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

	article = soup.find( class_ = 'full-article' )
	if article == None:
		return processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	processor.decompose_all( article.find_all( 'script' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'meta-category' ), False )
	datetime_list = processor.collect_datetime_objects( article.find_all( 'time' ), 'datetime' )
	author = processor.collect_text( article.find( itemprop = 'author' ), False )
	title = processor.collect_text( article.find( itemprop = 'name headline' ), False )
	ingress = processor.collect_text( article.find( class_ = 'ingress' ), False )
	images = processor.collect_images( article.find_all( 'img' ), 'data-src', '' )
	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	processor.decompose_all( article.find_all( class_ ='flexslider') )

	text = processor.collect_text( article.find( class_ = 'articlepart-1' ), False )

	return processor.create_dictionary('Verkkouutiset', url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.verkkouutiset.fi/talous/ammattisijoittajan_neuvot-33352", file('verkkouutiset.txt', 'w'))
