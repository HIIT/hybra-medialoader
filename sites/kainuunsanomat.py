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
	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose_all( article.find_all( class_ = 'attImage' ) )

	meta = article.find( 'time' )

	category = meta.find( 'b' )
	categories = [processor.collect_text( category )]
	category.decompose()

	datetime_list = processor.collect_datetime( meta, '' )

	author_tag = article.find( class_ = 'Kirjoittaja' )
	author = processor.collect_text( author_tag )
	author_tag.decompose()

	title = processor.collect_text( article.find( 'h1' ) )
	ingress = processor.collect_text( article.find( class_ = 'Alaotsikko' ) )
	text = processor.collect_text( article.find( class_ = 'Teksti' ) )
	images = processor.collect_images( article.find_all( 'img' ), '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'featuredCaption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.kainuunsanomat.fi/kainuun-sanomat/kotimaa/lipponen-moitti-sipilan-puheita-ministerien-vahentamisesta/", file('kainuunsanomat.txt', 'w'))
