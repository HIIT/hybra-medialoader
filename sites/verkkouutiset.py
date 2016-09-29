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

	ingress = soup.find_all( class_ = 'ingress')
	text = soup.find_all( class_='articlepart-1' )
	for slides in text[0].find_all( class_ ='flexslider'):
		slides.decompose()
	content = ingress[0].get_text(' ', strip = True)
	content += ' ' + text[0].get_text(' ', strip = True)
	text = processor.process(content)

	return processor.create_dictionary(url, http_status, '', [''], [''], '', '', '', text, [''], [''])

if __name__ == '__main__':
	parse("http://www.verkkouutiset.fi/talous/ammattisijoittajan_neuvot-33352", file('verkkouutiset.txt', 'w'))
