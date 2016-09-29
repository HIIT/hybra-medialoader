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

	text = soup.find_all( class_='post-content' )

	text[0].find('ul', {'class' : 'single-post-date'}).decompose()
	text[0].find('div', {'class' : 'keywords-block'}).decompose()
	for div in text[0].find_all( 'div', {'class' : 'share-buttons-block'} ):
		div.decompose()
	text[0]('p')[-1].decompose()
	text[0].footer.decompose()

	content = text[0].get_text(' ', strip=True)
	content = processor.process(content)

	media_content = { 'url' : str( ''.encode('utf8') ),
					  'http' : str( http_status ).encode('utf8'),
					  'category' : str( ''.encode('utf8') ),
					  'date' : [''],
					  'time' : [''],
					  'title' : str( ''.encode('utf8') ),
					  'ingress' : str( ''.encode('utf8') ),
					  'text' : str( ''.encode('utf8') ),
					  'images' : [''],
					  'captions' : [''] }
	return media_content

if __name__ == '__main__':

	parse("http://demokraatti.fi/sdpn-karna-maamme-ei-kesta-enaa-toista-samanlaista-paaministeria/", file('demokraatti.txt', 'w'))
