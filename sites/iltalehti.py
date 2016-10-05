import requests
import processor
from bs4 import BeautifulSoup
from datetime import datetime

def parse( url ):

	r = requests.get( url )

	http_status = r.status_code
	if r.status_code == 404:
		return

	r.encoding = 'iso-8859-1'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( 'isense' )
	text[0].find('div', {'class' : 'kainalo'}).decompose()
	text[0].find('div', {'class' : 'author'}).decompose()
	text[0].find('div', {'class' : 'kp-share-area'}).decompose()
	text = text[0].get_text(' ', strip=True)
	text = processor.process(text)

	return processor.create_dictionary(url, http_status, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':

	parse("http://www.iltalehti.fi/uutiset/2014120218885176_uu.shtml", file('iltalehti.txt', 'w'))
