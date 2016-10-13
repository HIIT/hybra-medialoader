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

	article = soup.find( class_ = 'mainArticle-content-wrapper' )
	processor.decompose_scripts( article )

	header = article.find( id = 'main-article-header' )
	categories = [str( header.find( class_ = 'section' ).get_text( strip = True ).encode('utf8') )]

	published = header.find( class_ = 'publish-date' ).get_text( strip = True )
	updated = header.find( class_ = 'updated-date' )
	if ( type(updated) != None ):
		updated = updated.get_text( strip = True )
		updated = updated.split(' ')
	datetime_list = [datetime.date(datetime.strptime(updated[1], "%d.%m.%Y")), datetime.date(datetime.strptime(published, "%d.%m.%Y"))]

	author = article.find( class_ = 'authorName' ).get_text( strip = True )
	title = article.find( class_ = 'main-article-header' ).get_text( strip = True )
	text = processor.collect_text( article, 'class', 'body')

	article.find( class_ = 'authorPicture' ).decompose()

	images = processor.collect_images( article, '', '' )
	captions = processor.collect_image_captions( article, 'class', 'main-media-caption' )

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, '', text, images, captions)

if __name__ == '__main__':

	parse("http://www.ess.fi/uutiset/talous/2014/12/03/perinteikas-konepaja-kaatui-venajan-kauppaan?ref=uutiset-section-teaser-latestCurrent-teaserCategoryMain", file('ess.txt', 'w'))
