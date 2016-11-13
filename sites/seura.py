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

	article = soup.find( class_ = 'article' )
	processor.decompose_all( article.find_all( 'script' ) )

	category_div = article.find( class_ = 'article-category' )
	categories = processor.collect_categories( category_div.find_all( 'a' ), False )

	datetime_list = processor.collect_datetime( article.find( class_ = 'article-meta' ), '' )
	author = processor.collect_text( article.find( class_ = 'article-credits' ), False )
	title = processor.collect_text( article.find( class_ = 'article-title' ), False )
	ingress = processor.collect_text( article.find( class_ = 'article-ingress' ), False )
	text = processor.collect_text( article.find( class_ = 'article-body' ), False )
	images = processor.collect_images_by_parent( article.find_all( class_ = 'fotorama head' ), '' )

	captions = [None]
	for caption_div in article.find_all( class_ = 'fotorama head' ):
		caption = BeautifulSoup( caption_div.find( 'a' )['data-caption'], "html.parser" )
		captions.append( processor.collect_text( caption, False ) )
	captions.pop(0)

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://seura.fi/puheenaihe/ajankohtaista/vasemmisto-kehuu-kokoomusta-harjoittavat-rehellisesti-politiikkaa-joka-on-ajanut-suomen-lamaan/?shared=43026-ad87bd06-500", file('seura.txt', 'w'))
