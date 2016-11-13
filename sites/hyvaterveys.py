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

	article = soup.find( 'article' )

	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( class_ = 'region bottom' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'field-name-field-category' ), False )
	datetime_list = processor.collect_datetime( article.find( class_ = 'field-name-post-date' ), 'timedate' )
	author = processor.collect_text( article.find( class_ = 'field-name-field-author' ), False )
	title = processor.collect_text( article.find( 'h1' ), False )
	ingress = processor.collect_text( article.find( class_ = 'field-name-field-summary' ), False )
	text = processor.collect_text( article.find( class_ = 'field-name-field-body' ), False )
	images = processor.collect_images( article.find_all( 'img' ), 'src', '')
	captions = processor.collect_image_captions( article.find_all( class_ = 'file-image-description-caption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':

	parse("http://www.hyvaterveys.fi/artikkeli/blogit/paljain_jaloin_pariisissa/eriavien_mielipiteiden_merkityksesta", file('hyvaterveys.txt', 'w'))
