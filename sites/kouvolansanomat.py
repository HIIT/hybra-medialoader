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

	article = soup.find( class_ = 'news-item' )
	if article == None:
		return processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	processor.decompose_all( article.find_all( 'script' ) )

	menu = soup.find( id = 'menu2' )
	categories = processor.collect_categories( menu.find_all( class_ = 'selected' ), False )

	datetime_list = processor.collect_datetime( article.find( class_ = 'date' ), '' )
	author = processor.collect_text( article.find( class_ = 'author' ), True )
	title = processor.collect_text( article.find( 'h1' ), False )
	images = processor.collect_images( article.find_all( 'img' ), 'src', 'http://www.kouvolansanomat.fi' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'caption' ) )

	processor.decompose_all( article.find_all( class_ = 'img_wrapper' ) )

	text = processor.collect_text( article.find( id = 'main_text' ), False )

	return processor.create_dictionary('Kouvolan sanomat', url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':
	parse("http://www.kouvolansanomat.fi/vaalit2015/2015/04/14/Ennakko%C3%A4%C3%A4nestys%20vilkkaampaa%20kuin%20edellisiss%C3%A4%20vaaleissa%20%E2%80%94%20kolmasosa%20kouvolalaisista%20on%20jo%20%C3%A4%C3%A4nest%C3%A4nyt/20151430/386", file('kouvolansanomat.txt', 'w'))
