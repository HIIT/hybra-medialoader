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
	processor.decompose( article.find( class_ = 'listingNewsBox' ) )

	categories = processor.collect_categories( soup.find_all( class_ = 'active' ), False )
	datetime_list = processor.collect_datetime( article.find( class_ = 'date' ), '' )
	title = processor.collect_text( article.find( class_ = 'newsHeadline' ), False )
	ingress = processor.collect_text( article.find( class_ = 'lead'), False )
	text = processor.collect_text( article.find( class_ = 'articleBody' ), False )
	images = processor.collect_images( article.find_all( 'img' ), 'http://www.ilkka.fi' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'newsImgText' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, '', title, ingress, text, images, captions)

if __name__ == '__main__':

	parse( 'http://www.ilkka.fi/uutiset/kotimaa/vertailu-suomessa-kolmanneksi-vahiten-korruptiota-1.1731397', file('ilkka.txt', 'w') )
