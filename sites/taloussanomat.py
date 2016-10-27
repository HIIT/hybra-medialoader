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

	article = soup.find( class_ = 'single-article' )
	processor.decompose_all( article.find_all( 'script' ) )

	categories = processor.collect_categories( soup.find( class_ = 'section-title' ), False )
	datetime_list = processor.collect_datetime( article.find( 'time' ), '' )
	author = processor.collect_text( article.find( class_ = 'byline' ), False )
	title = processor.collect_text( article.find( itemprop = 'headline name' ), False )
	ingress = processor.collect_text( article.find( class_ = 'ingress' ), False )
	text = processor.collect_text( article.find( class_ = 'body' ), False )
	images = processor.collect_images( article.find_all( 'img' ), 'src', '' )
	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.taloussanomat.fi/politiikka/2015/03/16/kreikka-lyhennamme-velkaamme-sovitusti-imflle/20153273/12", file('taloussanomat.txt', 'w'))
