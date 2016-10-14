# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	# Somethin weird is going on with this site; check later

	r = requests.get( url )
	if r.status_code == 404:
		processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	#for p in soup.find_all( class_='teksti' ):
	#	for string in p.stripped_strings:
	#    		out.write( string.encode('utf8') + ' ' )

	return processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

if __name__ == '__main__':
	parse("http://www.suomenmaa.fi/etusivu/7399391.html", file('suomenmaa.txt', 'w'))
