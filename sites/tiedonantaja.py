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

	article = soup.find( 'main' )
	if article == None:
		return processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])
	
	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose_all( article.find_all( class_ = 'nosto' ) )

	links = article.find( class_ = 'links' )
	categories = processor.collect_categories( links.find_all( 'li' ), False )

	datetime_list = processor.collect_datetime( article.find( class_ = 'field-name-field-publish-date' ), '' )
	author = processor.collect_text( article.find( class_ = 'tekija' ), False )
	title = processor.collect_text( article.find( id = 'page-title' ), False )
	text = processor.collect_text( article.find( class_ = 'body' ), False )
	images = processor.collect_images( article.find( class_ = 'views-field-field-op-main-image' ).find_all( 'img' ), 'src', '' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, [''])

if __name__ == '__main__':
	parse("http://www.tiedonantaja.fi/artikkelit/tarinoita-v-kivallasta", file('tiedonantaja.txt', 'w'))
