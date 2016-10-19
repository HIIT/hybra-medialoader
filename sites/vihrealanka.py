# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( class_ = 'node-wrap' )
	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( class_ = 'kredIso' ) )
	processor.decompose_all( article.find_all(class_ = 'tyrkkyBox') )
	processor.decompose( article.find( class_ = 'avainsanat' ) )
	processor.decompose( article.find( class_ = 'twitter-share-button' ) )
	processor.decompose( article.find( class_ = 'fb-like' ) )
	processor.decompose( article('h4')[-1] )

	meta = article.find( class_ = 'juttutiedot' )

	datetime_string = meta.find( class_ = 'aikaleima' ).get_text( strip = True )
	datetime_object = datetime.strptime( datetime_string, '%d.%m.%Y %H.%M')
	datetime_list = [datetime_object]

	author = processor.collect_text( meta.find( class_ = 'author' ) )
	meta.decompose()

	title_div = article.find( 'h2' )
	title = processor.collect_text( title_div )
	title_div.decompose()

	images = processor.collect_images( article.find_all( 'img' ), '')
	captions = processor.collect_image_captions( article.find_all( class_ = 'kuvaTekstiIso' ) )

	processor.decompose_all( article.find_all( class_ = 'kuvaTekstiIso' ) )

	text = processor.collect_text( article )

	return processor.create_dictionary(url, r.status_code, [''], datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.vihrealanka.fi/blogi-eno-vastaa/onko-tonnikalassa-myrkkyj%C3%A4", file('vihrealanka.txt', 'w'))
