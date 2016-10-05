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

	ingress = soup.find_all( class_='ingress')
	text = soup.find_all( class_='body' )
	for script in text[0].find_all('script'):
		script.decompose()
	for url in text[0].find_all('span', {'class' : 'print-url'}):
		url.decompose()
	content = ingress[0].get_text(' ', strip=True)
	content += ' ' + text[0].get_text(' ', strip=True)
	text = processor.process(content)

	return processor.create_dictionary(url, http_status, [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':
	parse("http://www.iltasanomat.fi/ulkomaat/art-1288789081654.html", file('iltasa.txt', 'w'))
