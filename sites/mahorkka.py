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

	article = soup.find( class_ = 'post' )
	processor.decompose_all( article.find_all( 'script' ) )
	for quote in article.find_all( 'blockquote' ):
		quote.decompose()
	article.find( class_ = 'author-avatar' ).decompose()
	article.find( id = 'after-single-post-widget-zone-single-post' ).decompose()
	article.find( id = 'sidebar' ).decompose()

	category = article.find( class_ = 'articleSection category' ).get_text( strip = True )
	categories = [str( category.encode('utf8') )]

	datetime_object = article.find( 'time' )['datetime'].replace( 'T' , ' ' )
	datetime_object = datetime_object.split( '+' )[0]
	datetime_list = [datetime_object]

	author = article.find( class_ = 'author' ).get_text( strip = True )
	title = article.find( class_ = ' xt-post-title' ).get_text( strip = True )
	text = processor.collect_text( article, 'class', 'post-body' )
	images = processor.collect_images( article, '', '', '' )
	captions = processor.collect_image_captions( article, '', 'figcaption' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.mahorkka.com/pavel-astahov-sai-lahtea-mutta-kuka-on-venajan-uusi-lapsiasiamies/", file('mahorkka.txt', 'w'))
