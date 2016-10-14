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

	article = soup.find( class_ = 'main-content-area' )
	processor.decompose_scripts( article )

	meta = article.find( class_ = 'post-meta' )

	category_tag = meta.find( class_ = 'category' )
	category = category_tag.get_text( strip = True )
	category_tag.decompose()
	categories = [str( category.encode('utf8') )]

	datetime_string = meta.get_text( ' ', strip = True )
	datetime_string = datetime_string.replace( ' Päivitetty '.decode('utf8'), ',' )
	datetime_data = datetime_string.split( ',' )
	datetime_list = [None]
	if len( datetime_data ) > 1:
		if len( datetime_data[1] ) < 6:
			datetime_data[1] = datetime_data[0].split( ' ' )[0] + ' ' + datetime_data[1]
	for datetime_string in datetime_data:
		date, time = datetime_string.split( ' ' )
		if len( date ) < 7:
			date = date + '2016'
		datetime_object = datetime.strptime( date + ' ' + time, '%d.%m.%Y %H.%M')
		datetime_list.append( datetime_object )
	datetime_list.pop(0)
	datetime_list.reverse()

	author = article.find( class_ = 'Kirjoittaja' ).get_text( strip = True )
	title = article.find( class_ = 'Otsikko' ).get_text( strip = True )
	ingress= article.find( class_ = 'Alaotsikko' ).get_text( strip = True )
	images = processor.collect_images( article, '', '', '' )
	captions = processor.collect_image_captions( article, 'class', 'caption' )

	for img_frame in article.find_all( class_ = 'kuvavaraus-wrapper' ):
		img_frame.decompose()

	text = processor.collect_text( article, 'class', 'Teksti')

	return processor.create_dictionary(url, r.status_code, categories, datetime_list, author, title, ingress, text, images, captions)

if __name__ == '__main__':
	parse("http://www.lapinkansa.fi/Lappi/1194944697007/artikkeli/kaunis+tykky+voi+olla+kavala+puille.html", file('lapinkansa.txt', 'w'))
