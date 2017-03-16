# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import processor

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( class_ = 'article-content')
	if article == None:
		return processor.create_dictionary('', url, r.status_code, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	processor.decompose_all( article.find_all( 'script' ) )
	processor.decompose( article.find( class_ = 'related-articles-container' ) )

	categories = processor.collect_categories( article.find_all( class_ = 'category' ) )

	datetime_data = article.find( class_ = 'post-meta' )
	processor.decompose( datetime_data.find( class_ = 'category' ) )
	processor.decompose( datetime_data.find( class_ = 'updated' ) )
	datetime_list = processor.collect_datetime( datetime_data )

	author = processor.collect_text( article.find( class_ = 'author--main') )
	title = processor.collect_text( article.find( class_ = 'heading--main' ) )
	images = processor.collect_images( article.find_all( 'img' ), 'src', '' )
	captions = processor.collect_image_captions( article.find_all( class_ = 'caption' ) )

	processor.decompose_all( article.find_all( class_ = 'image-wrapper' ) )
	text = processor.collect_text( article.find( class_ = 'content--main' ) )

	return processor.create_dictionary('Aamulehti', url, r.status_code, categories, datetime_list, author, title, u'', text, images, captions)


def parse_from_archive(url, content):

	article = BeautifulSoup( content, "html.parser" )

	if article == None:
		return processor.create_dictionary('Aamulehti', url, 404, [u''], [u''], u'', u'', u'', u'', [u''], [u''])

	meta = article.find( class_ = 'hakutuloslahde' )

	datetime_list = processor.collect_datetime( meta )

	category = processor.collect_text( meta ).split(',')[1].strip()
	subcat = processor.collect_text( article.find( class_ = 'jalkirivi' ) )
	subsubcat = processor.collect_text( article.find( class_ = 'esirivi' ) )

	categories = []
	for c in [category, subcat, subsubcat]:
		if c:
			categories.append(c)

	title = processor.collect_text( article.find( class_ = 'otsikko' ) )

	text_divs = article.find_all( class_ = 'artikkelip')
	text = ''
	for text_content in text_divs:
		text += processor.collect_text(text_content) + ' '
	text = processor.process( text.strip() )
	text += processor.collect_text( article.find( class_ = 'korjaus' ) )

	captions = processor.collect_image_captions( article.find_all( class_ = 'kuva') )

	return processor.create_dictionary('Aamulehti', url, 200, categories, datetime_list, u'', title, u'', text, [u''], captions)


if __name__ == '__main__':
	parse("http://www.aamulehti.fi/kotimaa/vanhemmat-uhmaavat-tamperelaisen-koulun-ohjetta-odotetaan-sita-paivaa-etta-joku-jaa-auton-alle/")
