import requests
from bs4 import BeautifulSoup
import processor

def parse( url ):

	r = requests.get( url )

	http_status = r.status_code
	if r.status_code == 404:
		return

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	article = soup.find( class_ = 'view-news-item')
	title = article.find( class_ = 'views-field-title' ).get_text().strip()
	category = article.find( class_ = 'views-field-field-aamuset-category').get_text().strip()

	datetime = article.find( class_ = 'views-field-field-aamuset-category').parent.find_all('div')[3]
	datetime = datetime.get_text().strip()
	datetime = datetime.split(' ')
	datetime_list = [None] * len(datetime)
	i = 0
	for string in datetime:
		datetime_list[i] = string
		i += 1
	if ( len(datetime_list) > 2 ):
		date = [str( datetime_list[3].encode('utf8') ), str( datetime_list[0].encode('utf8') )]
		time = [str( datetime_list[4].replace(')','').encode('utf8') ), str( datetime_list[1].encode('utf8') )]
	else:
		date = [str( datetime_list[0].encode('utf8') )]
		time = [str( datetime_list[1].encode('utf8') )]

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

	return processor.create_dictionary(url, http_status, category, date, time, '', title, '', text, image_src, captions_text)

if __name__ == '__main__':

	parse("http://www.aamuset.fi/naista-puhutaan/politiikka/yrttiaho-kanteli-oikeuskanslerille-nato-sopimuksesta", file('aamuset.txt', 'w'))
