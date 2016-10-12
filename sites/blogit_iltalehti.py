# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( 'article' )
	processor.decompose_scripts( article )

	title = article.find( class_ = 'entry-title' ).get_text().strip()

	url_elements = url.split('/')
	year = url_elements[4]
	month = url_elements[5]
	day = url_elements[6]
	datetime_list = [datetime.date(datetime.strptime(day + '.' + month + '.' + year, "%d.%m.%Y"))]

	author = article.find( class_ = 'author vcard' ).get_text().strip()
	text = processor.collect_text( article, 'class', 'entry-content' )

	return processor.create_dictionary(url, r.status_code, [''], datetime_list, author, title, '', text, [''], [''])

if __name__ == '__main__':

	parse("http://blogit.iltalehti.fi/eija-riitta-korhola/2015/03/15/visioni-helsingista-kansainvalinen-metropoli/", file('blogit.txt', 'w'))
