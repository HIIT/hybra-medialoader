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

	text = soup.find_all( class_ = 'Teksti' )
	text[0].find('p', {'class' : 'Kirjoittaja'}).decompose()
	text[0].find('p', {'class' : 'Paikka'}).decompose()
	text = text[0].get_text(' ', strip=True)
	text = processor.process(text)

	return processor.create_dictionary(url, http_status, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':
	parse("http://www.kainuunsanomat.fi/kainuun-sanomat/kotimaa/lipponen-moitti-sipilan-puheita-ministerien-vahentamisesta/", file('kainuunsanomat.txt', 'w'))
