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
	processor.decompose_all( soup.find_all( class_ = 'pohja' ) )
	processor.decompose_all( soup.find_all( class_ = 'footer_left') )
	processor.decompose_all( soup.find_all( class_ = 'keski_footer') )
	processor.decompose_all( soup.find_all( class_ = 'right_footer') )

	categories = [processor.collect_text( soup.find( class_ = 'vinjetti' ), False )]
	processor.decompose_all( soup.find_all( class_ = 'vinjetti' ) )

	datetime_list = processor.collect_datetime( soup.find( class_ = 'datetime' ).parent.parent, '' )
	author = processor.collect_text( soup.find( class_ = 'text-editor' ), False )
	title = processor.collect_text( soup.find( class_ = 'otsikko' ), False )
	ingress = processor.collect_text( soup.find( class_ = 'alarivi' ), False )

	processor.decompose_all( soup.find_all( class_ = 'alarivi' ) )

	text = ''
	for paragraph in soup.find_all( class_='teksti' ):
		paragraph_text = processor.collect_text( paragraph, False )
		if paragraph_text not in text:
			text = text + ' ' + paragraph_text
	text = text.strip()

	images = processor.collect_images( soup.find( class_ = 'pikkukuva' ).find_all( 'img' ), 'data-aghref', 'http://www.suomenmaa.fi/' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, [''])

if __name__ == '__main__':
	parse("http://www.suomenmaa.fi/etusivu/7399391.html", file('suomenmaa.txt', 'w'))
