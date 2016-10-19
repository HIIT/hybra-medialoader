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
	processor.decompose_all( article.find_all( 'blockquote' ) )
	processor.decompose( article.find( class_ = 'author-avatar' ) )
	processor.decompose( article.find( id = 'after-single-post-widget-zone-single-post' ) )
	processor.decompose( article.find( id = 'sidebar' ) )

	categories = [processor.collect_text( article.find( class_ = 'articleSection category' ) )]

	datetime_object = article.find( 'time' )['datetime'].replace( 'T' , ' ' )
	datetime_object = datetime_object.split( '+' )[0]
	datetime_list = [datetime_object]

	author = processor.collect_text( article.find( itemprop = 'name' ) )
	title = processor.collect_text( article.find( class_ = ' xt-post-title' ) )
	text = processor.collect_text( article.find( class_ = 'post-body' ) )
	images = processor.collect_images( article.find_all( 'img' ), '' )
	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.mahorkka.com/pavel-astahov-sai-lahtea-mutta-kuka-on-venajan-uusi-lapsiasiamies/", file('mahorkka.txt', 'w'))
