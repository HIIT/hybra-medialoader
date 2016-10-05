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

	text = soup.find_all('isense')
	for script in text[0].find_all('script'):
		script.decompose()
	text = text[0].get_text(' ', strip=True)
	text = processor.process(text)

	return processor.create_dictionary(url, http_status, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':
	parse("http://www.kaleva.fi/uutiset/kotimaa/asukkaat-vaativat-junille-nopeusrajoitusta-viime-yona-pamahti-niin-etta-pelkasin-hirren-menneen-poikki/683116/", file('kaleva.txt', 'w'))
