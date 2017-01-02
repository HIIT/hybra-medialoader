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
	if article == None:
		return processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	processor.decompose_all( article.find_all( 'script' ) )

	title = processor.collect_text( article.find( class_ = 'entry-title' ), False )

	url_elements = url.split('/')
	year = url_elements[4]
	month = url_elements[5]
	day = url_elements[6]
	datetime_list = [datetime.date(datetime.strptime(day + '.' + month + '.' + year, "%d.%m.%Y"))]

	author = processor.collect_text( article.find( class_ = 'author vcard' ), False )
	text = processor.collect_text( article.find( class_ = 'entry-content' ), False )

	return processor.create_dictionary('Iltalehti Blogit', url, r.status_code, [u''], datetime_list, author, title, u'', text, [u''], [u''])

if __name__ == '__main__':

	parse("http://blogit.iltalehti.fi/eija-riitta-korhola/2015/03/15/visioni-helsingista-kansainvalinen-metropoli/", file('blogit.txt', 'w'))
