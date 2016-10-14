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

	article = soup.find( class_ = 'article-container' )
	processor.decompose_scripts( article )
	article.find( class_ = 'article__related' ).decompose()

	meta = processor.process( article.find( class_ = 'news__meta' ).get_text( ' ', strip = True ) )
	meta = meta.replace( ' | Päivitetty '.decode('utf8'), ',' )

	meta = meta.split( ' ', 1 )
	categories = [str( meta[0].encode('utf8') )]

	meta = meta[1].rsplit( ' ', 1)
	datetime_data = meta[0].split( ',' )
	datetime_list = [None]
	for datetime_string in datetime_data:
		datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H:%M' )
		datetime_list.append( datetime_object )
	datetime_list.pop(0)
	datetime_list.reverse()

	author = meta[1]
	title = article.find( 'h1' ).get_text( strip = True )

	text = processor.collect_text( article, 'class', 'article__text' )
	images = processor.collect_images( article, '', '', '' )
	captions = processor.collect_image_captions( article, 'class', 'image__caption' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.kaleva.fi/uutiset/kotimaa/asukkaat-vaativat-junille-nopeusrajoitusta-viime-yona-pamahti-niin-etta-pelkasin-hirren-menneen-poikki/683116/", file('kaleva.txt', 'w'))
