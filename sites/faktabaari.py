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

	article = soup.find( id = 'main-content' )

	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( class_ = 'reviewpic' ) )

	datetime_list = processor.collect_datetime( article.find( class_ = 'published' ), '' )
	author = processor.collect_text( article.find( class_ = 'author' ) )
	title = processor.collect_text( article.find( 'h1' ) )
	text = processor.collect_text( article.find( class_ = 'entry-content' ) )
	images = processor.collect_images( article.find_all( 'img' ), '' )

	return processor.create_dictionary(url, r.status_code, [''], datetime_list, author, title, '', text, images, [''])

if __name__ == '__main__':

	parse("http://faktabaari.fi/fakta/petrus-pennanen-energiewende-oli-kaynnissa-jo-2002/", file('faktabaari.txt', 'w'))
