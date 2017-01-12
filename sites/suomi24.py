# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return {}

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	thread = soup.find( class_ = 'thread')

	info = thread.find( class_ = 'user-info-big' )

	answers = thread.find_all( class_ = 'answer-block-container' )

	print info.find( class_ = 'user-info-name' ).get_text( strip = True )
	print info.find( class_ = 'user-info-role' ).get_text( strip = True )
	print info.find( class_ = 'user-info-timestamp' ).get_text( strip = True )
	print thread.find( class_ = 'thread-text' ).get_text( strip = True )
	print 'answers ' + str(len(answers))

	# Näiden lisäksi breadcrumbs (topics), otsikko, viestien tykkäykset

	return {}

if __name__ == '__main__':
	parse("http://keskustelu.suomi24.fi/t/14671537/sioille-helmia")
