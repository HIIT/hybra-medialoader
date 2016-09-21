import requests

from bs4 import BeautifulSoup

def parse( url , out ):

	r = requests.get( url )
	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	for teksti in soup.find_all( class_='field field-name-body field-type-text-with-summary field-label-hidden' ):
		for p in teksti.find_all( 'p' ):

			for string in p.stripped_strings:
	        		out.write( string.encode('utf8') + ' ' )

if __name__ == '__main__':
	parse("http://www.uusisuomi.fi/kotimaa/79148-ex-ministeri-kummastelee-jotkut-pitavat-lahes-rikollisena", file('uusisuomi.txt', 'w'))
