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

	article = soup.find( class_ = 'article__full' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'article__meta__category' ) )

	title = processor.collect_text( article.find( class_ = 'medium-title' ) )

	datetime_list = []
	for teaser in soup.find_all( class_ = 'article-teaser__wrapper--wide' ):
		meta_title = processor.collect_text( teaser.find( class_ =  'small-title' ) )
		if meta_title == title:
			datetime_list = processor.collect_datetime( teaser.find( class_ = 'teaser__meta__timestamp' ) )

	author = processor.collect_text( article.find( class_ = 'author__name' ) )
	ingress = processor.collect_text( article.find( class_ = 'lead') )

	text = ''
	for string in article.find_all( 'p' ):
		text += ' ' + processor.collect_text( string )
	text = text.strip()

	images = processor.collect_images( article.find_all( 'img' ), 'src', 'http://www.ilkka.fi' )

	captions = []
	for caption_element in article.find_all( lambda tag: tag.name == 'a' and 'data-caption' in tag.attrs):
		captions.append( caption_element['data-caption'] )

	return processor.create_dictionary('Ilkka', url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':

	parse( 'https://www.ilkka.fi/uutiset/talous/kauhajokelainen-serres-osti-puolet-oululaisesta-firmasta-1.2211765' )
