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

	article = soup.find( class_ = 'post-single' )
	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( class_ = 'avatar' ) )

	categories = [processor.collect_text( article.find( itemprop = 'articleSection' ) )]

	datetime_data = article.find( itemprop = 'dateCreated datePublished' ).get_text( strip = True ).split( ' ' )
	if len( datetime_data[0] ) < 7:
		datetime_data[0] = datetime_data[0] + '2016'
	datetime_string = datetime_data[0] + ' ' + datetime_data[1]
	datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H:%M' )
	datetime_list = [datetime_object]

	author = processor.collect_text( article.find( rel = 'author' ) )
	title = processor.collect_text( article.find( itemprop = 'headline' ) )
	images = processor.collect_images( article.find_all( 'img' ), '')
	captions = processor.collect_image_captions( article.find_all( class_ = 'sopuli-image-caption' ) )

	processor.decompose_all( article.find_all( itemprop = 'associatedMedia' ) )
	text = processor.collect_text( article.find( itemprop = 'articleBody' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.kokemaenjokilaakso.fi/2015/03/16/kokemaen-siltala-esittaa-vihreaa-valoa-teljan-kaupungille/", file('kokemaenjokilaakso.txt', 'w'))
