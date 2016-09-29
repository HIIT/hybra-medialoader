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
	for img in text[0].find_all( class_ = 'kuvavaraus-wrapper' ):
		img.decompose()
	text = text[0].get_text(' ', strip = True)
	text = processor.process(text)
	return processor.create_dictionary(url, http_status, '', [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':
	parse("http://www.lapinkansa.fi/Lappi/1194944697007/artikkeli/kaunis+tykky+voi+olla+kavala+puille.html", file('lapinkansa.txt', 'w'))
