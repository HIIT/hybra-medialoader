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

	article = soup.find( class_ = 'single-article' )
	processor.decompose_all( article.find_all( 'script' ) )

	date, time = article.find( 'time' ).get_text( strip = True ).split( ' ' )
	if len( date ) < 7:
		date = date + '2016'
	datetime_object = datetime.strptime( date + ' ' + time, '%d.%m.%Y %H:%M')
	datetime_list = [datetime_object]

	author = processor.collect_text( article.find( class_ = 'byline' ) )
	title = processor.collect_text( article.find( itemprop = 'headline name' ) )
	ingress = processor.collect_text( article.find( class_ = 'ingress' ) )
	text = processor.collect_text( article.find( class_ = 'body' ) )
	images = processor.collect_images( article.find_all( 'img' ), '' )
	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	return processor.create_dictionary(url, r.status_code, [''], datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.taloussanomat.fi/politiikka/2015/03/16/kreikka-lyhennamme-velkaamme-sovitusti-imflle/20153273/12", file('taloussanomat.txt', 'w'))
