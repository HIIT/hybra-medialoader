# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	api_path = 'http://yle.fi/ylex/api/article/'

	_id = url.split( url )[-1]

	r = requests.get( api_path + _id )
	r = r.json()

	if r.status_code == 404:
		processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	authors = map( labda x:['name'] , r['authors'] )
	return processor.create_dictionary(url, r.status_code, [r['homesection']['name']], [ r['dateModified'], r['datePublished'] ], authors, r['title'], r['lead'], r['text'], [''], [''])

if __name__ == '__main__':
	parse("http://yle.fi/ylex/uutiset/ylexaan_tulossa_politiikan_superviikot__myos_sina_voit_tentata_paattajia_ennen_vaaleja/3-7875448", file('yle.txt', 'w'))
