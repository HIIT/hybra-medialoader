import requests
from bs4 import BeautifulSoup
import processor
from datetime import datetime

def parse( url ):

	r = requests.get( url )

	http_status = r.status_code
	if r.status_code == 404:
		return

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( class_ = 'view-news-item')

	categories = [str( article.find( class_ = 'views-field-field-aamuset-category').get_text().strip() ).encode('utf8')]

	datetime_data = article.find( class_ = 'views-field-field-aamuset-category').parent.find_all('div')[3]
	datetime_data = datetime_data.get_text(' ', strip = True)
	datetime_data = datetime_data.replace(')', '').split(' ')
	if len( datetime_data ) > 2:
		datetime_data.pop(2)
	datetime_list = [None]
	i = 0
	while i < len(datetime_data) - 1:
		date_string = datetime_data[i]
		time_string = datetime_data[i + 1]
		datetime_object = datetime.strptime( date_string + ' ' + time_string, "%d.%m.%Y %H:%M" )
		datetime_list.append(datetime_object)
		i += 2
	datetime_list.pop(0)
	datetime_list.reverse()

	author = article.find( class_  = 'views-field-field-visiting-journalist' ).get_text().strip()

	title = article.find( class_ = 'views-field-title' ).get_text().strip()

	text = article.find_all( class_='views-field views-field-body' )
	text = text[0].get_text(' ', strip=True)
	text = processor.process(text)

	imageframes = article.find_all(class_ = 'views-field-field-aamuset-images')
	image_src = [None] * len(imageframes)
	i = 0
	for frame in imageframes:
		img = frame.find('img')
		image_src[i] = str( img['src'].encode('utf8') )
		i += 1

	captions = article.find_all( class_ = 'views-field-field-aamuset-caption-1')
	captions_text = [None] * len(imageframes)
	i = 0
	for caption in captions:
		captions_text[i] = str( caption.get_text().strip().encode('utf8') )
		i += 1

	return processor.create_dictionary(url, http_status, categories, datetime_list, author, title, '', text, image_src, captions_text)

if __name__ == '__main__':

	parse("http://www.aamuset.fi/naista-puhutaan/politiikka/yrttiaho-kanteli-oikeuskanslerille-nato-sopimuksesta", file('aamuset.txt', 'w'))
