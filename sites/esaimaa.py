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

	text = soup.find_all( id='main_text' )
	for div in text[0].find_all( 'div', {'class' : 'lahde'} ):
		div.decompose()
	text = text[0].get_text(' ', strip=True)
	text = processor.process(text)

	return processor.create_dictionary(url, http_status, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':

	parse("http://www.esaimaa.fi/vaalit/2015/04/14/Kolumni%3A%20Mit%C3%A4%20tied%C3%A4mme%20p%C3%A4%C3%A4ministerist%C3%A4/2015118896734/478", file('esaimaa.txt', 'w'))
