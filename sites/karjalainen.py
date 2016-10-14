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

	meta = article.find( class_ = 'category_date' )

	category = meta.find( 'a' ).get_text( strip = True )
	categories = [str( category.encode('utf8') )]

	datetime_string = meta.find( 'time' ).get_text( strip = True )
	datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H:%M' )
	datetime_list = [datetime_object]

	author = article.find( class_ = 'author_credits' ).get_text( strip = True )
	title = article.find( 'h1' ).get_text( strip = True )
	text = processor.collect_text( article, 'class', 'itemFullText')
	images = processor.collect_images( article, '', '', 'http://www.karjalainen.fi' )
	captions = processor.collect_image_captions( article, 'class', 'itemImageCaption' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.karjalainen.fi/uutiset/uutis-alueet/kotimaa/item/71016-arhinmaen-perheeseen-syntymassa-lapsi-puheenjohtaja-ei-osallistu-vaalitilaisuuksiin", file('karjalainen.txt', 'w'))
