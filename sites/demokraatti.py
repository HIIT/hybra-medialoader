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

	article = soup.find('article')
	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( class_ = 'keywords-block' ) )
	processor.decompose_all( article.find_all( class_ = 'share-buttons-block' ) )
	processor.decompose( article('p')[-1] )
	processor.decompose( article.footer )
	processor.decompose( article.find( class_ = 'wp-user-avatar' ) )

	categories = [processor.collect_text( article.find( class_ = 'category' ) )]

	date = str( article.find( class_ = 'date' ).get_text().strip() )
	time = str( article.find( class_ = 'time' ).get_text().strip() )
	datetime_list = [datetime.strptime(date + ' ' + time, "%d.%m.%Y %H:%M")]

	processor.decompose( article.find( class_ = 'single-post-date' ) )

	author = processor.collect_text( article.find( class_ = 'post-author' ).find( 'li' ) )
	title = processor.collect_text( article.find( class_ = 'entry-title' ) )
	text = processor.collect_text( article.find( class_ = 'post-content' ) )
	images = processor.collect_images( article.find_all( 'img' ), 'https://demokraatti.fi' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, [''])

if __name__ == '__main__':

	parse("http://demokraatti.fi/sdpn-karna-maamme-ei-kesta-enaa-toista-samanlaista-paaministeria/", file('demokraatti.txt', 'w'))
