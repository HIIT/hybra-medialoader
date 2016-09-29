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

	text = soup.find_all( class_ = 'Teksti' )

	text[0].find('p', {'class' : 'Kirjoittaja'}).decompose()
	text[0].find('p', {'class' : 'Paikka'}).decompose()

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
	parse("http://www.kainuunsanomat.fi/kainuun-sanomat/kotimaa/lipponen-moitti-sipilan-puheita-ministerien-vahentamisesta/", file('kainuunsanomat.txt', 'w'))
