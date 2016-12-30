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

	article = soup.find( class_ = 'article-body-container' )
	if article == None:
		return processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose_all( article.find_all( class_ = 'photographer' ) )
	processor.decompose( article.find( class_ = 'linked-articles' ) )
	processor.decompose_all( article.find_all( 'aside' ) )
	processor.decompose( article.find( class_ = 'pagehitcounter' ) )
	processor.decompose( article.find( class_ = 'article-paywall' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'section-name' ), False )
	datetime_list = processor.collect_datetime( article.find( itemprop = 'datePublished' ), '' )
	author = processor.collect_text( article.find( class_ = 'author' ), False )
	title = processor.collect_text( article.find( 'h1' ), False )
	ingress = processor.collect_text( article.find( class_ = 'article-ingress' ), False )
	images = processor.collect_images( article.find_all( 'img' ), 'src', 'http:' )
	captions = processor.collect_image_captions( article.find_all( itemprop = 'caption' ), True )

	processor.decompose_all( article.find_all( class_ = 'embedded-image' ) )

	text = processor.collect_text( article.find( class_ = 'body' ), False )

	return processor.create_dictionary('Helsingin Sanomat', url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':

	parse("http://www.hs.fi/paakirjoitukset/a1428030701507", file('hs.txt', 'w'))
