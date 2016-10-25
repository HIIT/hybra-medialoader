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

	article = soup.find( class_ = 'full-article' )
	processor.decompose_all( article.find_all( 'script' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'meta-category' ) )
	datetime_list = processor.collect_datetime_objects( article.find_all( 'time' ), 'datetime' )
	author = processor.collect_text( article.find( itemprop = 'author' ) )
	title = processor.collect_text( article.find( itemprop = 'name headline' ) )
	ingress = processor.collect_text( article.find( class_ = 'ingress' ) )

	images = [None]
	for img in article.find_all( 'img' ):
		images.append( '' + str( img['data-src'].encode('utf8') ) )
	images.pop(0)

	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	processor.decompose_all( article.find_all( class_ ='flexslider') )

	text = processor.collect_text( article.find( class_ = 'articlepart-1' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.verkkouutiset.fi/talous/ammattisijoittajan_neuvot-33352", file('verkkouutiset.txt', 'w'))
