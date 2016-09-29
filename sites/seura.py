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

	text = soup.find_all( class_='article-body' )
	text = text[0].get_text(' ', strip = True)
	text = processor.process(text)

	return processor.create_dictionary(url, http_status, '', [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':
	parse("http://seura.fi/puheenaihe/ajankohtaista/vasemmisto-kehuu-kokoomusta-harjoittavat-rehellisesti-politiikkaa-joka-on-ajanut-suomen-lamaan/?shared=43026-ad87bd06-500", file('seura.txt', 'w'))
