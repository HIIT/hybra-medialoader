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

	article = soup.find( class_ = 'article' )
	processor.decompose_all( article.find_all( 'script' ) )

	categories = [None]
	category_div = article.find( class_ = 'article-category' )
	for category in category_div.find_all( 'a' ):
		categories.append( processor.collect_text( category ) )
	categories.pop(0)

	published = article.find( class_ = 'date' ).get_text( strip = True )
	updated = article.find( class_ = 'longerdate' )
	datetime_data = [published]
	if updated != None:
		updated = updated.get_text( strip = True ).replace( 'Päivitetty'.decode('utf8'), '' )
		datetime_data.append( updated )

	datetime_list = [None]
	for datetime_string in datetime_data:
		datetime_list.append( datetime.date( datetime.strptime( datetime_string, '%d.%m.%Y' ) ) )
	datetime_list.pop(0)
	datetime_list.reverse()

	author = processor.collect_text( article.find( class_ = 'article-credits' ) )
	title = processor.collect_text( article.find( class_ = 'article-title' ) )
	ingress = processor.collect_text( article.find( class_ = 'article-ingress' ) )
	text = processor.collect_text( article.find( class_ = 'article-body' ) )
	images = processor.collect_images_by_parent( article.find_all( class_ = 'fotorama head' ), '' )

	captions = [None]
	for caption_div in article.find_all( class_ = 'fotorama head' ):
		caption = BeautifulSoup( caption_div.find( 'a' )['data-caption'], "html.parser" )
		captions.append( processor.collect_text( caption ) )
	captions.pop(0)

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://seura.fi/puheenaihe/ajankohtaista/vasemmisto-kehuu-kokoomusta-harjoittavat-rehellisesti-politiikkaa-joka-on-ajanut-suomen-lamaan/?shared=43026-ad87bd06-500", file('seura.txt', 'w'))
