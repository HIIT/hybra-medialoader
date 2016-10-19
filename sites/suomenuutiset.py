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
	processor.decompose_all( article.find_all( class_ = 'somebar' ) )
	processor.decompose( article.find( class_ = 'tags' ) )

	categories = [processor.collect_text( article.find( class_ = 'post-category' ) )]

	date_string = article.find( class_ = 'date' ).get_text( strip = True )
	date_string = date_string.replace( ', ', '-' ).replace( ' ', '-' )
	month = date_string.split( '-' )[0]
	date_string = date_string.replace( month, processor.convert_month( month ) )
	time_string = article.find( class_ = 'time' ).get_text( strip = True )
	datetime_object = datetime.strptime( date_string + ' ' + time_string, '%m-%d-%Y %H:%M' )
	datetime_list = [datetime_object]

	author_div = article.find( class_ = 'article-page-writer' )
	author = processor.collect_text( author_div )
	author_div.decompose()

	title = processor.collect_text( article.find( class_ = 'post-title' ) )
	text = processor.collect_text( article.find( class_ = 'post-content' ) )
	images = processor.collect_images( article.find_all( 'img' ), '' )
	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("https://www.suomenuutiset.fi/perussuomalaiset-hurjassa-nosteessa-puoluesihteeri-ei-yllattynyt/", file('suomenuutiset.txt', 'w'))
