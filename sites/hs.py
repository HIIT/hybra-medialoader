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

	text = soup.find_all( class_ = "article-text-content" )

	for div in text[0].find_all( 'div'):
		div.decompose()

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

	parse("http://www.hs.fi/paakirjoitukset/a1428030701507", file('hs.txt', 'w'))
