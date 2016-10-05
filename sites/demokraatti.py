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

	article = soup.find('article')
	article.find('div', {'class' : 'keywords-block'}).decompose()
	for div in article.find_all( 'div', {'class' : 'share-buttons-block'} ):
		div.decompose()
	article('p')[-1].decompose()
	article.footer.decompose()
	article.find( class_ = 'post-author' ).decompose()

	title = article.find( class_ = 'entry-title' ).get_text().strip()
	categories = [str( article.find( class_ = 'category' ).get_text().strip().encode('utf8') )]
	date = [ str( article.find( class_ = 'date' ).get_text().strip().encode('utf8') ) ]
	time = [ str( article.find( class_ = 'time' ).get_text().strip().encode('utf8') ) ]

	text = article.find_all( class_='post-content' )
	text[0].find('ul', {'class' : 'single-post-date'}).decompose()
	text = text[0].get_text(' ', strip=True)
	text = processor.process(text)

	images = article.find_all( 'img' )
	image_src = [None] * len( images )
	i = 0
	for img in images:
		src = "https://demokraatti.fi" + img['src']
		image_src[i] = str( src.encode('utf8') )
		i += 1

	return processor.create_dictionary(url, http_status, categories, [''], '', title, '', text, image_src, [''])

if __name__ == '__main__':

	parse("http://demokraatti.fi/sdpn-karna-maamme-ei-kesta-enaa-toista-samanlaista-paaministeria/", file('demokraatti.txt', 'w'))
