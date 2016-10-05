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

	lead = soup.find_all( class_='lead')
	text = soup.find_all( class_='articleBody' )
	text[0]('p')[-1].decompose()
	content = lead[0].get_text(' ', strip=True)
	content += ' ' + text[0].get_text(' ', strip=True)
	text = processor.process(content)

	return processor.create_dictionary(url, http_status, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':

	parse( 'http://www.ilkka.fi/uutiset/kotimaa/vertailu-suomessa-kolmanneksi-vahiten-korruptiota-1.1731397', file('ilkka.txt', 'w') )
