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

	article = soup.find( class_ = 'article-container' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( class_ = 'article__related' ) )

	meta = article.find( class_ = 'news__meta' )

	categories = [ processor.collect_text( meta, False ).split( ' ' )[0] ]
	datetime_list = processor.collect_datetime( meta, '' )
	author = processor.collect_text( meta.find( class_ = 'news__source' ), False )
	title = processor.collect_text( article.find( 'h1' ), False )
	text = processor.collect_text( article.find( class_ = 'article__text' ), False )
	images = processor.collect_images( article.find_all( 'img' ), 'src', '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'image__caption' ) )

	return processor.create_dictionary('Kaleva', url, r.status_code, categories, datetime_list, author, title, u'', text, images, captions)

if __name__ == '__main__':
	parse("http://www.kaleva.fi/uutiset/kotimaa/asukkaat-vaativat-junille-nopeusrajoitusta-viime-yona-pamahti-niin-etta-pelkasin-hirren-menneen-poikki/683116/", file('kaleva.txt', 'w'))
