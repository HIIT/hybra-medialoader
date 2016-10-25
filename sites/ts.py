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

	meta = article.find( class_ = 'tsv3-c-common-article__meta__row1' )

	categories = processor.collect_categories( meta.find_all( 'a' ) )
	datetime_list = processor.collect_datetime_objects( meta.find_all( 'time' ), 'datetime' )
	author = processor.collect_text( article.find( class_ = 'kirjoittaja' ) )
	title = processor.collect_text( article.find( class_ = 'otsikko' ) )
	text = processor.collect_text( article.find( class_ = 'tsv3-c-common-article__textitem tsv3-c-common-article__textitem--teksti' ) )
	images = processor.collect_images( article.find_all( 'img' ), 'http://www.ts.fi' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'tsv3-c-common-article__attachment__info__caption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.ts.fi/eduskuntavaalit/750980/Start+up+yrittaja+kuplii+innostusta", file('ts.txt', 'w'))
