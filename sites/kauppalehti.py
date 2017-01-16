# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

    api_path = 'https://www.kauppalehti.fi/api/news/article/'
    _id = url.split( '/' )[-1]

    r = requests.get( api_path + _id )
    if r.status_code == 404:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

    r.encoding = 'UTF-8'

    json = r.json()

    categories = [processor.process( json['mainCategory']['name'] )]
    datetime_list = processor.collect_datetime_json( json, 'published', 'modified' )
    author = processor.process( json['byline'][0] )
    title = processor.process( json['title'] )
    ingress = processor.process( json['headline'] )

    text_html = BeautifulSoup( json['body'], "html.parser" )
    text = processor.collect_text( text_html )

    if 'keyImage' in json:
        image_url = 'http://images.kauppalehti.fi/547x/http:' + json['keyImage']
        images = [image_url]
    else:
        images = [u'']

    return processor.create_dictionary('Kauppalehti', url, r.status_code, categories, datetime_list, author, title, ingress, text, images, [u''])

if __name__ == '__main__':
	parse("http://www.kauppalehti.fi/uutiset/putin-nayttaytyi-julkisuudessa-ilman-juoruja-olisi-tylsaa/pBBPEhQ2?ext=ampparit", file('kauppalehti.txt', 'w'))
