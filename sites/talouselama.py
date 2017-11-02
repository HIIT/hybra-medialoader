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

	root = soup.find( id = 'root' )
	article_container = root.contents[0].contents[1].contents[3]

	article = article_container.contents[0].contents[2].contents[2]
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'aside' ) )

	categories = processor.collect_categories( [article.find( 'h4' )] )
	datetime_list = processor.collect_datetime( article.contents[0] )
	title = processor.collect_text( article.find( 'h1' ) )

	text_section = article.find( 'section' )
	ingress = processor.collect_text( text_section.find( 'h3' ) )
	text_container = text_section.contents[0].contents[5]
	text = processor.collect_text( text_container )

	images = processor.collect_images( [article.find( 'img' )], 'src', '')
	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	return processor.create_dictionary('Talouselämä', url, r.status_code, categories, datetime_list, u'', title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("https://www.talouselama.fi/uutiset/rovion-expomo-peter-vesterbacka-siirtyy-opetuspelifirmaan/6d78f191-2018-3abb-86c0-0b4eefa1f267")
