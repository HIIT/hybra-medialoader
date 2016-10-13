# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find('article')
	processor.decompose_scripts( article )
	article.find('div', {'class' : 'keywords-block'}).decompose()
	for div in article.find_all( 'div', {'class' : 'share-buttons-block'} ):
		div.decompose()
	article('p')[-1].decompose()
	article.footer.decompose()
	article.find( class_ = 'wp-user-avatar' ).decompose()

	categories = [str( article.find( class_ = 'category' ).get_text().strip().encode('utf8') )]

	date = str( article.find( class_ = 'date' ).get_text().strip() )
	time = str( article.find( class_ = 'time' ).get_text().strip() )
	datetime_list = [datetime.strptime(date + ' ' + time, "%d.%m.%Y %H:%M")]

	article.find('ul', {'class' : 'single-post-date'}).decompose()

	author = article.find( class_ = 'post-author' ).find( 'li' ).get_text(' ', strip = True)
	title = article.find( class_ = 'entry-title' ).get_text( strip = True )
	text = processor.collect_text( article, 'class', 'post-content' )
	images = processor.collect_images( article, '', 'https://demokraatti.fi' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, [''])

if __name__ == '__main__':

	parse("http://demokraatti.fi/sdpn-karna-maamme-ei-kesta-enaa-toista-samanlaista-paaministeria/", file('demokraatti.txt', 'w'))
