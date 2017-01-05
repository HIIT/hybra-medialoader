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

	article = soup.find( class_ = 'mainArticle-content-wrapper' )
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )

	header = article.find( id = 'main-article-header' )
	categories = processor.collect_categories( header.find_all( class_ = 'section' ), False )
	datetime_list = processor.collect_datetime( article.find( class_ = 'article-date' ), '' )
	author = processor.collect_text( article.find( class_ = 'authorName' ), False )
	title = processor.collect_text( article.find( class_ = 'main-article-header' ), False )
	text = processor.collect_text( article.find( class_ = 'body' ), False )

	processor.decompose( article.find( class_ = 'authorPicture' ) )

	images = processor.collect_images( article.find_all( 'img' ), 'src', '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'main-media-caption' ) )

	return processor.create_dictionary('Etelä-Suomen Sanomat', url, r.status_code, categories, datetime_list, author, title, u'', text, images, captions)

if __name__ == '__main__':

	parse("http://www.ess.fi/uutiset/talous/2014/12/03/perinteikas-konepaja-kaatui-venajan-kauppaan?ref=uutiset-section-teaser-latestCurrent-teaserCategoryMain", file('ess.txt', 'w'))
