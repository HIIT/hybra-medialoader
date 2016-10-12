# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )

	http_status = r.status_code
	if r.status_code == 404:
		return

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( id = 'main-content' )
	for script in article.find_all( 'script' ):
		script.decompose()
	article.find( class_ = 'reviewpic' ).decompose()

	date = article.find( class_ = 'published').get_text( strip = True )
	datetime_list = [datetime.date( datetime.strptime( date, "%d.%m.%Y" ) )]

	author = article.find( class_ = 'author' ).get_text( strip = True )

	title = article.find( 'h1' ).get_text( strip = True )

	text = soup.find_all( class_='entry-content' )
	text = text[0].get_text(' ', strip=True)
	text = processor.process(text)

	images = article.find_all( 'img' )
	image_src = [None]
	for img in images:
		image_src.append( str( img['src'].encode('utf8') ) )
	image_src.pop(0)

	return processor.create_dictionary(url, http_status, [''], datetime_list, author, title, '', text, image_src, [''])

if __name__ == '__main__':

	parse("http://faktabaari.fi/fakta/petrus-pennanen-energiewende-oli-kaynnissa-jo-2002/", file('faktabaari.txt', 'w'))
