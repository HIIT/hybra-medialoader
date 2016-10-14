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
	processor.decompose_scripts( article )
	for div in article.find_all( class_ = 'somebar' ):
		div.decompose()
	article.find( class_ = 'tags' ).decompose()

	category = article.find( class_ = 'post-category' ).get_text( strip = True )
	categories = [str( category.encode('utf8') )]

	date_string = article.find( class_ = 'date' ).get_text( strip = True )
	date_string = date_string.replace( ', ', '-' ).replace( ' ', '-' )
	month = date_string.split( '-' )[0]
	date_string = date_string.replace( month, processor.convert_month( month ) )
	time_string = article.find( class_ = 'time' ).get_text( strip = True )
	datetime_object = datetime.strptime( date_string + ' ' + time_string, '%m-%d-%Y %H:%M' )
	datetime_list = [datetime_object]

	author_div = article.find( class_ = 'article-page-writer' )
	author = author_div.get_text( strip = True )
	author_div.decompose()

	title = article.find( class_ = 'post-title' ).get_text( ' ', strip = True )
	text = processor.collect_text( article, 'class', 'post-content' )
	images = processor.collect_images( article, '', '', '' )
	captions = processor.collect_image_captions( article, '', 'figcaption')

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("https://www.suomenuutiset.fi/perussuomalaiset-hurjassa-nosteessa-puoluesihteeri-ei-yllattynyt/", file('suomenuutiset.txt', 'w'))
