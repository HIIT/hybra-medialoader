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

	article = soup.find( 'article' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )

	datetime_list = processor.collect_datetime_objects( article.find_all( 'time' ), 'datetime' )

	author = processor.collect_text( article.find( class_ = 'posted-on' ) )
	author = author.replace( ' |', '' )

	processor.decompose( article.find( class_ = 'entry-meta' ) )

	title = processor.collect_text( article.find( class_ = 'entry-title' ) )

	ingress = processor.collect_text( article.find( class_ = 'entry-content__ingress' ) )
	processor.decompose( article.find( class_ = 'entry-content__ingress' ) )

	images = processor.collect_images( article.find_all( 'img' ), 'src', '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'entry-header__caption' ) )
	text = processor.collect_text( article.find( class_ = 'entry-content' ) )

	return processor.create_dictionary('Verkkouutiset', url, r.status_code, [u''], datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.verkkouutiset.fi/talous/ammattisijoittajan_neuvot-33352", file('verkkouutiset.txt', 'w'))
