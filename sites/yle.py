import requests
from bs4 import BeautifulSoup
import processor

def parse( url , out ):

	r = requests.get( url )

	if r.status_code == 404:
		return

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	text = soup.find_all( class_='yle__article__content' )

	for figure in text[0].find_all( 'figure' ):
		figure.decompose()

	content = text[0].get_text(' ', strip = True)
	content = processor.process(content)

	out.write( content.encode('utf8') )

if __name__ == '__main__':
	parse("http://yle.fi/uutiset/nordea_synkkyys_jatkuu/7663512", file('yle.txt', 'w'))
