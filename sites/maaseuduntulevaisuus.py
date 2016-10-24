# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime
import time

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		processor.create_dictionary(url, r.status_code, [''], [''], '', '', '', '', [''], [''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( 'article' )
	processor.decompose_all( article.find_all( 'script' ) )

	categories = [processor.collect_text( article.find( class_ = 'article-release-info__section' ) )]
	datetime_list = processor.collect_datetime( article.find( class_ = 'article-release-info__time' ), '' )
	author = processor.collect_text( article.find( itemprop = 'author' ) )

	title_div = article.find( class_ = 'article-single-heading' )
	title = processor.collect_text( title_div.find( 'h1' ) )
	ingress = processor.collect_text( title_div.find( 'p' ) )

	text = processor.collect_text( article.find( class_ = 'article-single-section__content' ) )
	images = processor.collect_images( article.find_all( 'img' ), 'http://www.maaseuduntulevaisuus.fi' )
	captions = processor.collect_image_captions( article.find_all( 'figcaption' ) )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.maaseuduntulevaisuus.fi/maatalous/nurmipelloille-voi-tulla-k%C3%A4ytt%C3%B6rajoituksia-1.76216", file('maaseudun.txt', 'w'))
