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
	processor.decompose_all( article.find_all('noscript') )
	processor.decompose( article.find( class_ = 'share-buttons' ) )
	processor.decompose( article.find( class_ = 'subscribe-newsletter' ) )

	categories = [processor.collect_text( article.find( class_ = 'kicker' ) )]

	date, time = article.find( class_ = 'timestamp' ).get_text( strip = True ).split( ' ' )
	if len( date ) < 7:
		date = date + '2016'
	datetime_object = datetime.strptime( date + ' ' + time, '%d.%m.%Y %H:%M')
	datetime_list = [datetime_object]

	author = processor.collect_text( article.find( class_ = 'author' ) )
	title = processor.collect_text( article.find( class_ = 'title' ) )
	text = processor.collect_text( article.find( class_ = 'article-body' ) )
	images = processor.collect_images( article.find_all( 'img' ), '')
	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.talouselama.fi/vaalit/vaalitebatti/murtuuko+suurten+puolueiden+valta++vaaliraati+vastaa/a2301513", file('talouselama.txt', 'w'))
