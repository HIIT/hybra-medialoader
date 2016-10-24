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

	article = soup.find( class_ = 'article-content' )
	processor.decompose_all( article.find_all( 'script' ) )

	meta = article.find( class_ = 'post-meta' )

	category_tag = meta.find( class_ = 'category' )
	categories = [processor.collect_text( category_tag )]
	category_tag.decompose()

	datetime_list = processor.collect_datetime( meta, '' )
	author = processor.collect_text( article.find( class_ = 'Kirjoittaja' ) )
	title = processor.collect_text( article.find( class_ = 'Otsikko' ) )
	text = processor.collect_text( article.find( class_ = 'Teksti' ) )
	images = processor.collect_images( article.find_all( 'img' ), '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'caption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.satakunnankansa.fi/Satakunta/1194972499877/artikkeli/myrsky+runteli+myos+vaalimainoksia.html", file('satakunnankansa.txt', 'w'))
