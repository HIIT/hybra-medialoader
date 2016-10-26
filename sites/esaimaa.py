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

	article = soup.find( class_ = 'news-item')
	processor.decompose_all( article.find_all( 'script' ) )

	categories = processor.collect_categories( soup.find( id = 'menu2' ).find( class_ = 'selected' ), False )
	datetime_list = processor.collect_datetime( article.find( class_ = 'date'), '' )

	author = article.find_all( class_ = 'lahde' )
	author = processor.process( author[0].get_text(' ', strip = True) + ' ' + author[1].get_text(' ', strip = True) )

	processor.decompose_all( article.find_all( class_ = 'lahde' ) )

	title = processor.collect_text( article.find('h1'), False )
	text = processor.collect_text( article.find( id = 'main_text' ), False )
	images = processor.collect_images( article.find_all( 'img' ), 'src', 'http://www.esaimaa.fi' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, [''])

if __name__ == '__main__':

	parse("http://www.esaimaa.fi/vaalit/2015/04/14/Kolumni%3A%20Mit%C3%A4%20tied%C3%A4mme%20p%C3%A4%C3%A4ministerist%C3%A4/2015118896734/478", file('esaimaa.txt', 'w'))
