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

	article = soup.find( class_ = 'article-content')
	article.find( class_ = 'related-articles-container' ).decompose()

	title = article.find( class_ = 'Otsikko' ).get_text().strip()

	category = article.find( class_ = 'category' ).get_text().strip()

	datetime = article.find( class_ = 'post-meta' )
	datetime.find( class_ = 'category' ).decompose()
	datetime.find( class_ = 'updated' ).decompose()

	datetime_list = [None] * 4
	i = 0
	for string in datetime.stripped_strings:
		datetime_list[i] = string
		i += 1

	if i > 1:
		date = [str( datetime_list[2].encode('utf8') ), str( datetime_list[0].encode('utf8') )]
		time = [str( datetime_list[3].encode('utf8') ), str( datetime_list[1].encode('utf8') )]
	else:
		date = [str( datetime_list[0].encode('utf8') )]
		time = [str( datetime_list[1].encode('utf8') )]

	images = article.find_all( 'img' )
	image_src = [None] * len(images)
	i = 0
	for img in images:
		image_src[i] = str( img['src'].encode('utf8') )
		i += 1

	captions = article.find_all( class_ = 'caption' )
	captions_text = [None] * len(captions)
	i = 0
	for caption in captions:
		captions_text[i] = str( caption.get_text().encode('utf8') )
		i += 1

	text = article.find( class_ = 'Teksti' )
	for div in text.find_all( class_ = 'kuvavaraus-wrapper' ):
		div.decompose()
	text = text.get_text(' ', strip = True)
	text = processor.process(text)

	media_content = { 'url' : str( url.encode('utf8') ),
					  'http' : str( http_status ).encode('utf8'),
					  'category' : str( category.encode('utf8') ),
					  'date' : date,
					  'time' : time,
					  'title' : str( title.encode('utf8') ),
					  'ingress' : str( '' ).encode('utf8'),
					  'text' : str( text.encode("utf8") ),
					  'images' : image_src,
					  'captions' : captions_text }
	return media_content

if __name__ == '__main__':

	parse("http://www.aamulehti.fi/kotimaa/vanhemmat-uhmaavat-tamperelaisen-koulun-ohjetta-odotetaan-sita-paivaa-etta-joku-jaa-auton-alle/", file('aamulehti.txt', 'w'))
