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

	text = soup.find_all( class_ = 'field field-name-body' )
	for script in text[0].find_all('script'):
		script.decompose()
	text = text[0].get_text(' ', strip=True)
	text = processor.process(text)

	return processor.create_dictionary(url, http_status, '', [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':

	parse("http://www.iltamakasiini.fi/artikkeli/279454-kauko-royhkaa-hairikoinyt-rokkari-ehdolla-eduskuntaan", file('iltamakasiini.txt', 'w'))
