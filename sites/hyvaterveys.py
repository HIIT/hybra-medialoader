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

	text = soup.find_all( class_ = "field-name-body" )
	text = text[0].get_text(' ', strip=True)
	text = processor.process(text)

	return processor.create_dictionary(url, http_status, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':

	parse("http://www.hyvaterveys.fi/artikkeli/blogit/paljain_jaloin_pariisissa/eriavien_mielipiteiden_merkityksesta", file('hyvaterveys.txt', 'w'))
