# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )
	processor.decompose_all( soup.find_all( class_ = 'pohja' ) )
	processor.decompose_all( soup.find_all( class_ = 'footer_left') )
	processor.decompose_all( soup.find_all( class_ = 'keski_footer') )
	processor.decompose_all( soup.find_all( class_ = 'right_footer') )
	processor.decompose_all( soup.find_all( class_ = 'sitaatti' ) )

	categories = [processor.collect_text( soup.find( class_ = 'vinjetti' ) )]
	processor.decompose_all( soup.find_all( class_ = 'vinjetti' ) )

	datetime_list = processor.collect_datetime( soup.find( class_ = 'datetime' ).parent.parent )
	datetime_list.reverse()

	author = processor.collect_text( soup.find( class_ = 'text-editor' ) )
	title = processor.collect_text( soup.find( class_ = 'otsikko' ) )
	ingress = processor.collect_text( soup.find( class_ = 'alarivi' ) )

	processor.decompose_all( soup.find_all( class_ = 'alarivi' ) )

	text = ''
	for paragraph in soup.find_all( class_='teksti' ):
		paragraph_text = processor.collect_text( paragraph )
		if paragraph_text not in text:
			text = text + ' ' + paragraph_text
	text = text.strip()

	img_div = soup.find( class_ = 'pikkukuva' )
	images = [u'']
	captions = [u'']
	if img_div:
		header_img = img_div.find_all( 'img' )
		images = processor.collect_images( header_img, 'data-aghref', 'http://www.suomenmaa.fi/' )
		captions = [header_img[0]['alt']]


	return processor.create_dictionary('Suomenmaa', url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.suomenmaa.fi/uutiset/merkelilla-ei-vaihtoehtoja--putin-ja-trump-pakottavat-hakemaan-jatkokautta-6.3.206004.f13da076a7")
