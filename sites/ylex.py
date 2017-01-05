# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	api_path = 'http://yle.fi/ylex/api/article/'
	_id = url.split( '/' )[-1]

	r = requests.get( api_path + _id )
	if r.status_code == 404:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	r.encoding = 'UTF-8'

	json = r.json()

	categories = [processor.process( json['homesection']['name'] )]
	datetime_list = processor.collect_datetime_json( json, 'datePublished', 'dateModified' )
	author = processor.process( json['authors'][0]['name'] )
	title = processor.process( json['title'] )
	ingress = processor.process( json['lead'] )

	text_html = BeautifulSoup( json['html'], "html.parser" )
	text = processor.collect_text( text_html, False )

	if 'image' in json:
		image_json = json['image']
		images = [image_json['uri']]
		captions = [image_json['alt']]
	else:
		images, captions = [u''], [u'']

	return processor.create_dictionary('Yle X', url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://yle.fi/ylex/uutiset/ylexaan_tulossa_politiikan_superviikot__myos_sina_voit_tentata_paattajia_ennen_vaaleja/3-7875448", file('yle.txt', 'w'))
