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

	article = soup.find( class_ = 'node-wrap' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( class_ = 'kredIso' ) )
	processor.decompose_all( article.find_all(class_ = 'tyrkkyBox') )
	processor.decompose( article.find( class_ = 'avainsanat' ) )
	processor.decompose( article.find( class_ = 'twitter-share-button' ) )
	processor.decompose( article.find( class_ = 'fb-like' ) )
	processor.decompose( article.find( class_ = 'moreLanka' ) )

	meta = article.find( class_ = 'juttutiedot' )
	datetime_list = processor.collect_datetime( meta, )
	author = processor.collect_text( meta.find( class_ = 'author' ) )
	processor.decompose( meta )

	title = processor.collect_text( article.find( 'h2' ), True )
	images = processor.collect_images( article.find_all( 'img' ), 'src', '')
	captions = processor.collect_image_captions( article.find_all( class_ = 'kuvaTekstiIso' ) )

	processor.decompose_all( article.find_all( class_ = 'kuvaTekstiIso' ) )

	text = processor.collect_text( article )

	return processor.create_dictionary('Vihreä lanka', url, r.status_code, [u''], datetime_list, author, title, u'', text, images, captions)

if __name__ == '__main__':
	parse("http://www.vihrealanka.fi/uutiset-ymp%C3%A4rist%C3%B6/sy%C3%B6mmek%C3%B6-tulevaisuudessa-ilmaa-ja-vett%C3%A4-suomalaishanke-lupaa-puolet-proteiinia", file('vihrealanka.txt', 'w'))
